from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Dataset(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    name: str
    filename: str
    columns: List[str]
    row_count: int
    date_column: Optional[str] = None
    target_column: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class ForecastRun(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    dataset_id: str
    model_type: str  # "linear_regression" or "random_forest"
    forecast_days: int
    metrics: Dict[str, float]  # MAE, RMSE, R2
    predictions: List[Dict[str, Any]]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Insight(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    dataset_id: str
    forecast_run_id: str
    insight_type: str  # "peak", "low", "trend", "seasonality"
    message: str
    data: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class APILog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    endpoint: str
    method: str
    status_code: int
    duration_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ForecastRequest(BaseModel):
    dataset_id: str
    date_column: str
    target_column: str
    model_type: str
    forecast_days: int = 30

class CompareRequest(BaseModel):
    forecast_ids: List[str]
