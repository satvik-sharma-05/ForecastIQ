"""
ML Engine for using pre-trained models with robust preprocessing
"""

import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, List, Any
from datetime import datetime, timedelta
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from data_preprocessor import DataPreprocessor

class PretrainedForecastEngine:
    
    def __init__(self):
        """Load pre-trained models"""
        self.models_dir = 'models'
        self.lr_model = None
        self.rf_model = None
        self.feature_columns = None
        self.metrics = None
        self.preprocessor = DataPreprocessor()
        
        self._load_models()
    
    def _load_models(self):
        """Load all pre-trained models and metadata"""
        try:
            lr_path = os.path.join(self.models_dir, 'linear_regression_model.pkl')
            rf_path = os.path.join(self.models_dir, 'random_forest_model.pkl')
            features_path = os.path.join(self.models_dir, 'feature_columns.pkl')
            metrics_path = os.path.join(self.models_dir, 'model_metrics.pkl')
            
            if os.path.exists(lr_path):
                self.lr_model = joblib.load(lr_path)
                print("✅ Loaded Linear Regression model")
            
            if os.path.exists(rf_path):
                self.rf_model = joblib.load(rf_path)
                print("✅ Loaded Random Forest model")
            
            if os.path.exists(features_path):
                self.feature_columns = joblib.load(features_path)
                print(f"✅ Loaded feature columns: {len(self.feature_columns)} features")
            
            if os.path.exists(metrics_path):
                self.metrics = joblib.load(metrics_path)
                print("✅ Loaded model metrics")
                
        except Exception as e:
            print(f"⚠️ Warning: Could not load pre-trained models: {e}")
            print("   Will fall back to on-the-fly training")
    
    def prepare_features(self, df: pd.DataFrame, date_col: str, target_col: str) -> pd.DataFrame:
        """Prepare features matching the training data"""
        
        # Aggregate to daily level
        agg_dict = {target_col: 'sum'}
        
        # Add optional columns if they exist
        optional_cols = ['Quantity', 'quantity', 'Profit', 'profit']
        for col in optional_cols:
            if col in df.columns:
                agg_dict[col] = 'sum'
        
        daily_data = df.groupby(date_col).agg(agg_dict).reset_index()
        
        # Rename columns to standard names
        daily_data.columns = ['date'] + [col.lower() for col in daily_data.columns[1:]]
        daily_data['sales'] = daily_data[target_col.lower()] if target_col.lower() in daily_data.columns else daily_data.iloc[:, 1]
        
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        daily_data = daily_data.sort_values('date')
        
        # Create time-based features
        daily_data['DayOfWeek'] = daily_data['date'].dt.dayofweek
        daily_data['Month'] = daily_data['date'].dt.month
        daily_data['Quarter'] = daily_data['date'].dt.quarter
        daily_data['Year'] = daily_data['date'].dt.year
        daily_data['DayOfYear'] = daily_data['date'].dt.dayofyear
        daily_data['WeekOfYear'] = daily_data['date'].dt.isocalendar().week.astype(int)
        daily_data['IsWeekend'] = (daily_data['DayOfWeek'] >= 5).astype(int)
        
        # Create lag features
        for lag in [1, 7, 14, 30]:
            daily_data[f'Sales_Lag_{lag}'] = daily_data['sales'].shift(lag)
        
        # Rolling averages
        daily_data['Sales_MA_7'] = daily_data['sales'].rolling(window=7, min_periods=1).mean()
        daily_data['Sales_MA_30'] = daily_data['sales'].rolling(window=30, min_periods=1).mean()
        
        # Add quantity and profit if they don't exist (use sales as proxy)
        if 'quantity' not in daily_data.columns:
            daily_data['quantity'] = daily_data['sales'] / daily_data['sales'].mean()
        if 'profit' not in daily_data.columns:
            daily_data['profit'] = daily_data['sales'] * 0.2  # Assume 20% profit margin
        
        return daily_data
    
    def predict_with_pretrained(self, df: pd.DataFrame, date_col: str, target_col: str, 
                                model_type: str, forecast_days: int) -> Dict[str, Any]:
        """Generate predictions using pre-trained models with robust preprocessing"""
        
        # Select model
        if model_type == "linear_regression":
            model = self.lr_model
            model_metrics = self.metrics.get('linear_regression', {}) if self.metrics else {}
        elif model_type == "random_forest":
            model = self.rf_model
            model_metrics = self.metrics.get('random_forest', {}) if self.metrics else {}
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        if model is None:
            raise ValueError(f"Model {model_type} not loaded. Please train models first.")
        
        # Use robust preprocessor
        print("🔄 Preprocessing data with robust pipeline...")
        result = self.preprocessor.process(
            df, 
            date_column=date_col,
            target_column=target_col,
            create_lags=True,
            create_rolling=True,
            scale_features=False
        )
        
        if not result['success']:
            raise ValueError(result['error'])
        
        daily_data = result['dataframe']
        detected_date_col = result['date_column']
        detected_target_col = result['target_column']
        
        print(f"✅ Preprocessing complete: {len(daily_data)} rows, {len(daily_data.columns)} columns")
        
        # Ensure all required features exist
        required_features = self.feature_columns
        missing_features = [f for f in required_features if f not in daily_data.columns]
        
        if missing_features:
            print(f"⚠️ Missing features: {missing_features}")
            # Create missing features with default values
            for feat in missing_features:
                if feat in ['quantity', 'profit']:
                    # Already handled in preprocessing
                    pass
                else:
                    daily_data[feat] = 0
        
        # Drop rows with NaN in required features
        daily_data = daily_data.dropna(subset=required_features)
        
        if len(daily_data) == 0:
            raise ValueError("Not enough data after removing missing values")
        
        print(f"✅ All {len(required_features)} features present")
        
        # Get last date for forecasting
        last_date = daily_data[detected_date_col].iloc[-1]
        
        # Get last row features in correct order
        last_row = daily_data[required_features].iloc[-1]
        
        # Generate future predictions
        predictions = []
        current_features = last_row.values.reshape(1, -1)
        
        for i in range(1, forecast_days + 1):
            # Predict next value
            pred_value = model.predict(current_features)[0]
            pred_date = last_date + timedelta(days=i)
            
            predictions.append({
                "date": pred_date.strftime("%Y-%m-%d"),
                "predicted_value": float(pred_value)
            })
            
            # Update time features for next prediction
            next_features = current_features.copy()
            
            # Update time-based features
            feature_updates = {
                'DayOfWeek': pred_date.dayofweek,
                'Month': pred_date.month,
                'Quarter': pred_date.quarter,
                'Year': pred_date.year,
                'DayOfYear': pred_date.timetuple().tm_yday,
                'WeekOfYear': pred_date.isocalendar()[1],
                'IsWeekend': 1 if pred_date.dayofweek >= 5 else 0
            }
            
            for feat_name, feat_value in feature_updates.items():
                if feat_name in required_features:
                    next_features[0, required_features.index(feat_name)] = feat_value
            
            # Update lag features (shift by one)
            if 'Sales_Lag_1' in required_features:
                next_features[0, required_features.index('Sales_Lag_1')] = pred_value
            
            current_features = next_features
        
        # Calculate metrics
        if model_metrics and 'test_mae' in model_metrics:
            metrics = {
                "mae": model_metrics['test_mae'],
                "rmse": model_metrics['test_rmse'],
                "r2": model_metrics['test_r2']
            }
        else:
            # Calculate on historical data
            X = daily_data[required_features].values
            y = daily_data['sales'].values
            
            split_idx = int(len(X) * 0.8)
            X_test = X[split_idx:]
            y_test = y[split_idx:]
            
            if len(X_test) > 0:
                y_pred = model.predict(X_test)
                metrics = {
                    "mae": float(mean_absolute_error(y_test, y_pred)),
                    "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
                    "r2": float(r2_score(y_test, y_pred))
                }
            else:
                metrics = {"mae": 0.0, "rmse": 0.0, "r2": 0.0}
        
        return {
            "metrics": metrics,
            "predictions": predictions
        }
    
    def generate_insights(self, df: pd.DataFrame, target_col: str, predictions: List[Dict]) -> List[Dict[str, Any]]:
        """Generate business insights from data and predictions"""
        insights = []
        
        # Standardize target column name
        target_col_lower = target_col.lower().strip().replace(' ', '_')
        
        # Try to find the target column (case-insensitive)
        actual_target_col = None
        for col in df.columns:
            if col.lower() == target_col_lower or col == target_col:
                actual_target_col = col
                break
        
        # If still not found, try 'sales' as fallback
        if actual_target_col is None:
            if 'sales' in df.columns:
                actual_target_col = 'sales'
            elif 'Sales' in df.columns:
                actual_target_col = 'Sales'
            else:
                # Use first numeric column
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    actual_target_col = numeric_cols[0]
                else:
                    return []  # No numeric columns, return empty insights
        
        # Historical analysis
        mean_val = df[actual_target_col].mean()
        max_val = df[actual_target_col].max()
        min_val = df[actual_target_col].min()
        
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
        recent_avg = df[actual_target_col].tail(7).mean()
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
