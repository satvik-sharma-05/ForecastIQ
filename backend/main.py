from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection, get_database
from models import *
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from ml_engine_pretrained import PretrainedForecastEngine
import pandas as pd
from datetime import datetime
from bson import ObjectId
import os
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    os.makedirs("uploads", exist_ok=True)
    
    # Initialize pre-trained forecast engine
    global forecast_engine
    forecast_engine = PretrainedForecastEngine()
    
    yield
    await close_mongo_connection()

app = FastAPI(title="ForecastIQ API", lifespan=lifespan)

# Global forecast engine
forecast_engine = None

# CORS Configuration - Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://forecast-iq-theta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# ==================== AUTH ROUTES ====================

@app.post("/api/auth/signup")
async def signup(user: UserCreate, db=Depends(get_database)):
    # Check if user exists
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_doc = {
        "email": user.email,
        "name": user.name,
        "hashed_password": get_password_hash(user.password),
        "created_at": datetime.now()
    }
    result = await db.users.insert_one(user_doc)
    
    # Generate token
    token = create_access_token(data={"sub": str(result.inserted_id)})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": str(result.inserted_id), "email": user.email, "name": user.name}
    }

@app.post("/api/auth/login")
async def login(credentials: UserLogin, db=Depends(get_database)):
    user = await db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(data={"sub": str(user["_id"])})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": str(user["_id"]), "email": user["email"], "name": user["name"]}
    }

@app.get("/api/auth/me")
async def get_me(user_id: str = Depends(get_current_user), db=Depends(get_database)):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(user["_id"]), "email": user["email"], "name": user["name"]}

# ==================== DATASET ROUTES ====================

@app.post("/api/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user),
    db=Depends(get_database)
):
    # Save file
    filename = f"{user_id}_{datetime.now().timestamp()}_{file.filename}"
    filepath = os.path.join("uploads", filename)
    
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Read and analyze with encoding fallback
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, encoding='latin-1')
        except:
            df = pd.read_csv(filepath, encoding='iso-8859-1')
    
    dataset_doc = {
        "user_id": user_id,
        "name": file.filename,
        "filename": filename,
        "columns": df.columns.tolist(),
        "row_count": len(df),
        "date_column": None,
        "target_column": None,
        "uploaded_at": datetime.now()
    }
    
    result = await db.datasets.insert_one(dataset_doc)
    dataset_doc["_id"] = result.inserted_id
    
    return {
        "id": str(result.inserted_id),
        "name": dataset_doc["name"],
        "columns": dataset_doc["columns"],
        "row_count": dataset_doc["row_count"],
        "uploaded_at": dataset_doc["uploaded_at"].isoformat()
    }

@app.get("/api/datasets")
async def get_datasets(user_id: str = Depends(get_current_user), db=Depends(get_database)):
    cursor = db.datasets.find({"user_id": user_id}).sort("uploaded_at", -1)
    datasets = await cursor.to_list(length=100)
    
    return [{
        "id": str(d["_id"]),
        "name": d["name"],
        "columns": d["columns"],
        "row_count": d["row_count"],
        "uploaded_at": d["uploaded_at"].isoformat()
    } for d in datasets]

@app.delete("/api/datasets/{dataset_id}")
async def delete_dataset(
    dataset_id: str,
    user_id: str = Depends(get_current_user),
    db=Depends(get_database)
):
    dataset = await db.datasets.find_one({"_id": ObjectId(dataset_id), "user_id": user_id})
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Delete file
    filepath = os.path.join("uploads", dataset["filename"])
    if os.path.exists(filepath):
        os.remove(filepath)
    
    await db.datasets.delete_one({"_id": ObjectId(dataset_id)})
    return {"message": "Dataset deleted"}

# ==================== FORECAST ROUTES ====================

@app.post("/api/forecast/run")
async def run_forecast(
    request: ForecastRequest,
    user_id: str = Depends(get_current_user),
    db=Depends(get_database)
):
    # Validate dataset
    dataset = await db.datasets.find_one({"_id": ObjectId(request.dataset_id), "user_id": user_id})
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Load data
    filepath = os.path.join("uploads", dataset["filename"])
    
    # Read with encoding fallback
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(filepath, encoding='latin-1')
        except:
            df = pd.read_csv(filepath, encoding='iso-8859-1')
    
    # Validate columns
    if request.date_column not in df.columns or request.target_column not in df.columns:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid columns. Available columns: {', '.join(df.columns.tolist())}"
        )
    
    # Run forecast with pre-trained models
    try:
        result = forecast_engine.predict_with_pretrained(
            df, request.date_column, request.target_column, request.model_type, request.forecast_days
        )
    except ValueError as e:
        # Better error message for date parsing issues
        if "datetime" in str(e).lower():
            raise HTTPException(
                status_code=400, 
                detail=f"Column '{request.date_column}' doesn't contain valid dates. Please select a date column. Available columns: {', '.join(df.columns.tolist())}"
            )
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast failed: {str(e)}")
    
    # Save forecast run
    forecast_doc = {
        "user_id": user_id,
        "dataset_id": request.dataset_id,
        "model_type": request.model_type,
        "forecast_days": request.forecast_days,
        "metrics": result["metrics"],
        "predictions": result["predictions"],
        "created_at": datetime.now()
    }
    forecast_result = await db.forecast_runs.insert_one(forecast_doc)
    forecast_id = str(forecast_result.inserted_id)
    
    # Generate insights
    insights_data = forecast_engine.generate_insights(df, request.target_column, result["predictions"])
    
    # Save insights
    for insight in insights_data:
        insight_doc = {
            "user_id": user_id,
            "dataset_id": request.dataset_id,
            "forecast_run_id": forecast_id,
            "insight_type": insight["type"],
            "message": insight["message"],
            "data": insight.get("data"),
            "created_at": datetime.now()
        }
        await db.insights.insert_one(insight_doc)
    
    return {
        "forecast_id": forecast_id,
        "metrics": result["metrics"],
        "predictions": result["predictions"],
        "insights": insights_data
    }

@app.get("/api/forecast/history")
async def get_forecast_history(
    user_id: str = Depends(get_current_user),
    db=Depends(get_database)
):
    cursor = db.forecast_runs.find({"user_id": user_id}).sort("created_at", -1).limit(50)
    runs = await cursor.to_list(length=50)
    
    result = []
    for run in runs:
        dataset = await db.datasets.find_one({"_id": ObjectId(run["dataset_id"])})
        result.append({
            "id": str(run["_id"]),
            "dataset_name": dataset["name"] if dataset else "Unknown",
            "model_type": run["model_type"],
            "forecast_days": run["forecast_days"],
            "metrics": run["metrics"],
            "created_at": run["created_at"].isoformat()
        })
    
    return result

@app.get("/api/forecast/{forecast_id}")
async def get_forecast_details(
    forecast_id: str,
    user_id: str = Depends(get_current_user),
    db=Depends(get_database)
):
    forecast = await db.forecast_runs.find_one({"_id": ObjectId(forecast_id), "user_id": user_id})
    if not forecast:
        raise HTTPException(status_code=404, detail="Forecast not found")
    
    # Get insights
    cursor = db.insights.find({"forecast_run_id": forecast_id})
    insights = await cursor.to_list(length=100)
    
    return {
        "id": str(forecast["_id"]),
        "model_type": forecast["model_type"],
        "forecast_days": forecast["forecast_days"],
        "metrics": forecast["metrics"],
        "predictions": forecast["predictions"],
        "insights": [{
            "type": i["insight_type"],
            "message": i["message"],
            "data": i.get("data")
        } for i in insights],
        "created_at": forecast["created_at"].isoformat()
    }

# ==================== COMPARISON ROUTES ====================

@app.post("/api/forecast/compare")
async def compare_forecasts(
    request: CompareRequest,
    user_id: str = Depends(get_current_user),
    db=Depends(get_database)
):
    if len(request.forecast_ids) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 forecasts to compare")
    
    forecasts = []
    for fid in request.forecast_ids:
        forecast = await db.forecast_runs.find_one({"_id": ObjectId(fid), "user_id": user_id})
        if forecast:
            forecasts.append({
                "id": str(forecast["_id"]),
                "model_type": forecast["model_type"],
                "metrics": forecast["metrics"],
                "predictions": forecast["predictions"]
            })
    
    # Determine best model
    best = min(forecasts, key=lambda x: x["metrics"]["mae"])
    
    return {
        "forecasts": forecasts,
        "best_model": {
            "id": best["id"],
            "model_type": best["model_type"],
            "reason": f"Lowest MAE: {best['metrics']['mae']:.2f}"
        }
    }

# ==================== INSIGHTS ROUTES ====================

@app.get("/api/insights")
async def get_insights(
    user_id: str = Depends(get_current_user),
    db=Depends(get_database)
):
    cursor = db.insights.find({"user_id": user_id}).sort("created_at", -1).limit(20)
    insights = await cursor.to_list(length=20)
    
    return [{
        "id": str(i["_id"]),
        "type": i["insight_type"],
        "message": i["message"],
        "data": i.get("data"),
        "created_at": i["created_at"].isoformat()
    } for i in insights]

# ==================== DASHBOARD STATS ====================

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(
    user_id: str = Depends(get_current_user),
    db=Depends(get_database)
):
    total_datasets = await db.datasets.count_documents({"user_id": user_id})
    total_forecasts = await db.forecast_runs.count_documents({"user_id": user_id})
    total_insights = await db.insights.count_documents({"user_id": user_id})
    
    # Get recent activity
    recent_forecasts = await db.forecast_runs.find({"user_id": user_id}).sort("created_at", -1).limit(5).to_list(5)
    
    return {
        "total_datasets": total_datasets,
        "total_forecasts": total_forecasts,
        "total_insights": total_insights,
        "recent_activity": [{
            "id": str(f["_id"]),
            "model_type": f["model_type"],
            "created_at": f["created_at"].isoformat()
        } for f in recent_forecasts]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
