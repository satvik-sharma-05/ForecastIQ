import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta

class ForecastEngine:
    
    @staticmethod
    def prepare_data(df: pd.DataFrame, date_col: str, target_col: str) -> Tuple[np.ndarray, np.ndarray]:
        """Convert dates to numeric features and prepare target"""
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.sort_values(date_col)
        
        # Create time-based features
        df['days_since_start'] = (df[date_col] - df[date_col].min()).dt.days
        
        X = df[['days_since_start']].values
        y = df[target_col].values
        
        return X, y, df[date_col].max()
    
    @staticmethod
    def train_and_predict(X: np.ndarray, y: np.ndarray, model_type: str, forecast_days: int, last_date: datetime) -> Dict[str, Any]:
        """Train model and generate predictions"""
        
        # Split data (80-20)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train model
        if model_type == "linear_regression":
            model = LinearRegression()
        elif model_type == "random_forest":
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        model.fit(X_train, y_train)
        
        # Calculate metrics
        y_pred = model.predict(X_test)
        metrics = {
            "mae": float(mean_absolute_error(y_test, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "r2": float(r2_score(y_test, y_pred))
        }
        
        # Generate future predictions
        last_day = X[-1][0]
        future_X = np.array([[last_day + i] for i in range(1, forecast_days + 1)])
        future_predictions = model.predict(future_X)
        
        # Format predictions
        predictions = []
        for i, pred in enumerate(future_predictions):
            pred_date = last_date + timedelta(days=i+1)
            predictions.append({
                "date": pred_date.strftime("%Y-%m-%d"),
                "predicted_value": float(pred)
            })
        
        return {
            "metrics": metrics,
            "predictions": predictions
        }
    
    @staticmethod
    def generate_insights(df: pd.DataFrame, target_col: str, predictions: List[Dict]) -> List[Dict[str, Any]]:
        """Generate business insights from data and predictions"""
        insights = []
        
        # Historical analysis
        mean_val = df[target_col].mean()
        max_val = df[target_col].max()
        min_val = df[target_col].min()
        
        # Peak detection
        if max_val > mean_val * 1.5:
            insights.append({
                "type": "peak",
                "message": f"Peak value detected: {max_val:.2f} (50% above average)",
                "data": {"value": float(max_val), "threshold": float(mean_val * 1.5)}
            })
        
        # Low period detection
        if min_val < mean_val * 0.5:
            insights.append({
                "type": "low",
                "message": f"Low demand period detected: {min_val:.2f} (50% below average)",
                "data": {"value": float(min_val), "threshold": float(mean_val * 0.5)}
            })
        
        # Trend analysis
        recent_avg = df[target_col].tail(7).mean()
        if recent_avg > mean_val * 1.2:
            insights.append({
                "type": "trend",
                "message": "Upward trend detected in recent data (20% above average)",
                "data": {"recent_avg": float(recent_avg), "overall_avg": float(mean_val)}
            })
        elif recent_avg < mean_val * 0.8:
            insights.append({
                "type": "trend",
                "message": "Downward trend detected in recent data (20% below average)",
                "data": {"recent_avg": float(recent_avg), "overall_avg": float(mean_val)}
            })
        
        # Future prediction insights
        pred_values = [p["predicted_value"] for p in predictions]
        future_avg = np.mean(pred_values)
        
        if future_avg > mean_val * 1.3:
            insights.append({
                "type": "forecast",
                "message": f"High demand expected: {future_avg:.2f} (30% above historical average)",
                "data": {"predicted_avg": float(future_avg), "historical_avg": float(mean_val)}
            })
        elif future_avg < mean_val * 0.7:
            insights.append({
                "type": "forecast",
                "message": f"Low demand expected: {future_avg:.2f} (30% below historical average)",
                "data": {"predicted_avg": float(future_avg), "historical_avg": float(mean_val)}
            })
        
        return insights
