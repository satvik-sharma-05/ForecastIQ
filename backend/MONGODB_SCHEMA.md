# ForecastIQ MongoDB Schema

## Collections Overview

### 1. users
Stores user account information
```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "name": "John Doe",
  "hashed_password": "bcrypt_hash",
  "created_at": ISODate
}
```

### 2. datasets
Stores uploaded dataset metadata
```json
{
  "_id": ObjectId,
  "user_id": "user_object_id",
  "name": "sales_data.csv",
  "filename": "userid_timestamp_sales_data.csv",
  "columns": ["date", "sales", "region"],
  "row_count": 365,
  "date_column": "date",
  "target_column": "sales",
  "uploaded_at": ISODate
}
```

### 3. forecast_runs
Stores each forecast execution with results
```json
{
  "_id": ObjectId,
  "user_id": "user_object_id",
  "dataset_id": "dataset_object_id",
  "model_type": "random_forest",
  "forecast_days": 30,
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
  "created_at": ISODate
}
```

### 4. insights
Auto-generated business insights
```json
{
  "_id": ObjectId,
  "user_id": "user_object_id",
  "dataset_id": "dataset_object_id",
  "forecast_run_id": "forecast_object_id",
  "insight_type": "peak",
  "message": "Peak value detected: 5000 (50% above average)",
  "data": {
    "value": 5000,
    "threshold": 3333
  },
  "created_at": ISODate
}
```

## Indexes (Recommended)

```javascript
// Users
db.users.createIndex({ "email": 1 }, { unique: true })

// Datasets
db.datasets.createIndex({ "user_id": 1, "uploaded_at": -1 })

// Forecast Runs
db.forecast_runs.createIndex({ "user_id": 1, "created_at": -1 })
db.forecast_runs.createIndex({ "dataset_id": 1 })

// Insights
db.insights.createIndex({ "user_id": 1, "created_at": -1 })
db.insights.createIndex({ "forecast_run_id": 1 })
```

## Key Features Enabled

✅ User authentication & authorization
✅ Multi-dataset management
✅ Forecast history tracking
✅ Model comparison
✅ Automated insights generation
✅ Dashboard statistics
