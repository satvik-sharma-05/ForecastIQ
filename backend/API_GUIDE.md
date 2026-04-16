# ForecastIQ API Guide

## Base URL
```
http://localhost:8000
```

## Authentication

All protected endpoints require Bearer token in header:
```
Authorization: Bearer <your_jwt_token>
```

---

## 🔐 Auth Endpoints

### Sign Up
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "name": "John Doe"
}

Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "...",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}
```

### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>
```

---

## 📁 Dataset Endpoints

### Upload Dataset
```http
POST /api/datasets/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <csv_file>

Response:
{
  "id": "dataset_id",
  "name": "sales_data.csv",
  "columns": ["date", "sales", "region"],
  "row_count": 365,
  "uploaded_at": "2026-04-16T10:30:00"
}
```

### Get All Datasets
```http
GET /api/datasets
Authorization: Bearer <token>
```

### Delete Dataset
```http
DELETE /api/datasets/{dataset_id}
Authorization: Bearer <token>
```

---

## 📊 Forecast Endpoints

### Run Forecast
```http
POST /api/forecast/run
Authorization: Bearer <token>
Content-Type: application/json

{
  "dataset_id": "...",
  "date_column": "date",
  "target_column": "sales",
  "model_type": "random_forest",
  "forecast_days": 30
}

Response:
{
  "forecast_id": "...",
  "metrics": {
    "mae": 45.23,
    "rmse": 67.89,
    "r2": 0.92
  },
  "predictions": [
    {
      "date": "2026-05-01",
      "predicted_value": 1234.56
    }
  ],
  "insights": [
    {
      "type": "peak",
      "message": "Peak value detected...",
      "data": {...}
    }
  ]
}
```

### Get Forecast History
```http
GET /api/forecast/history
Authorization: Bearer <token>

Response:
[
  {
    "id": "...",
    "dataset_name": "sales_data.csv",
    "model_type": "random_forest",
    "forecast_days": 30,
    "metrics": {...},
    "created_at": "2026-04-16T10:30:00"
  }
]
```

### Get Forecast Details
```http
GET /api/forecast/{forecast_id}
Authorization: Bearer <token>
```

---

## 🔍 Comparison Endpoints

### Compare Forecasts
```http
POST /api/forecast/compare
Authorization: Bearer <token>
Content-Type: application/json

{
  "forecast_ids": ["id1", "id2", "id3"]
}

Response:
{
  "forecasts": [...],
  "best_model": {
    "id": "...",
    "model_type": "random_forest",
    "reason": "Lowest MAE: 45.23"
  }
}
```

---

## 💡 Insights Endpoints

### Get All Insights
```http
GET /api/insights
Authorization: Bearer <token>

Response:
[
  {
    "id": "...",
    "type": "peak",
    "message": "Peak value detected: 5000",
    "data": {...},
    "created_at": "2026-04-16T10:30:00"
  }
]
```

---

## 📈 Dashboard Endpoints

### Get Dashboard Stats
```http
GET /api/dashboard/stats
Authorization: Bearer <token>

Response:
{
  "total_datasets": 5,
  "total_forecasts": 12,
  "total_insights": 24,
  "recent_activity": [...]
}
```

---

## Model Types

- `linear_regression` - Fast, simple baseline
- `random_forest` - Better accuracy, handles non-linearity

## Insight Types

- `peak` - High value detection
- `low` - Low value detection
- `trend` - Upward/downward trends
- `forecast` - Future predictions analysis
