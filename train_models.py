"""
ForecastIQ - Automated Model Training Script
Downloads datasets, trains models, and saves .pkl files
Run: python train_models.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import os
import sys

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print("="*70)
print("🚀 ForecastIQ - Automated Model Training")
print("="*70)

# Create directories
os.makedirs('backend/models', exist_ok=True)
os.makedirs('data', exist_ok=True)
os.makedirs('visualizations', exist_ok=True)

print("\n📁 Directories created successfully!")

# ============================================================================
# STEP 1: DOWNLOAD DATASETS
# ============================================================================

print("\n" + "="*70)
print("📥 STEP 1: Downloading Datasets")
print("="*70)

def download_superstore_dataset():
    """Download Superstore dataset from Kaggle"""
    try:
        print("\n🔄 Attempting to download Superstore dataset from Kaggle...")
        import kagglehub
        from kagglehub import KaggleDatasetAdapter
        
        file_path = "Sample - Superstore.csv"
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "vivek468/superstore-dataset-final",
            file_path
        )
        
        # Save locally
        df.to_csv('data/superstore.csv', index=False)
        print("✅ Superstore dataset downloaded successfully!")
        return df
    except Exception as e:
        print(f"❌ Failed to download from Kaggle: {e}")
        return None

def download_uci_retail_dataset():
    """Download UCI Online Retail dataset"""
    try:
        print("\n🔄 Attempting to download UCI Online Retail dataset...")
        from ucimlrepo import fetch_ucirepo
        
        online_retail = fetch_ucirepo(id=352)
        X = online_retail.data.features
        y = online_retail.data.targets
        df = pd.concat([X, y], axis=1)
        
        # Save locally
        df.to_csv('data/online_retail.csv', index=False)
        print("✅ UCI Online Retail dataset downloaded successfully!")
        return df
    except Exception as e:
        print(f"❌ Failed to download from UCI: {e}")
        return None

def use_sample_dataset():
    """Use the sample dataset if downloads fail"""
    try:
        print("\n🔄 Using sample dataset...")
        df = pd.read_csv('sample_sales_data.csv')
        print("✅ Sample dataset loaded successfully!")
        return df
    except Exception as e:
        print(f"❌ Failed to load sample dataset: {e}")
        return None

# Try to download datasets
df = download_superstore_dataset()

if df is None:
    print("\n⚠️ Kaggle download failed. Trying UCI dataset...")
    df = download_uci_retail_dataset()

if df is None:
    print("\n⚠️ UCI download failed. Using sample dataset...")
    df = use_sample_dataset()

if df is None:
    print("\n❌ ERROR: Could not load any dataset!")
    print("Please ensure you have:")
    print("  1. Kaggle API configured (kaggle.json in ~/.kaggle/)")
    print("  2. Or ucimlrepo installed (pip install ucimlrepo)")
    print("  3. Or sample_sales_data.csv in the root directory")
    sys.exit(1)

print(f"\n✅ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ============================================================================
# STEP 2: DATA EXPLORATION & CLEANING
# ============================================================================

print("\n" + "="*70)
print("🔍 STEP 2: Data Exploration & Cleaning")
print("="*70)

print("\nDataset Info:")
print(df.info())

print("\nFirst 5 rows:")
print(df.head())

# Detect date and sales columns
date_columns = []
sales_columns = []

for col in df.columns:
    col_lower = col.lower()
    if 'date' in col_lower or 'time' in col_lower:
        date_columns.append(col)
    if 'sales' in col_lower or 'revenue' in col_lower or 'amount' in col_lower:
        sales_columns.append(col)

print(f"\n📅 Detected date columns: {date_columns}")
print(f"💰 Detected sales columns: {sales_columns}")

# Use first detected columns or defaults
date_col = date_columns[0] if date_columns else 'date'
sales_col = sales_columns[0] if sales_columns else 'sales'

print(f"\n✅ Using: Date='{date_col}', Sales='{sales_col}'")

# Clean data
print("\n🧹 Cleaning data...")
df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
df = df.dropna(subset=[date_col, sales_col])
df = df.sort_values(date_col)

print(f"✅ Cleaned dataset: {df.shape[0]} rows")
print(f"📅 Date range: {df[date_col].min()} to {df[date_col].max()}")

# ============================================================================
# STEP 3: EXPLORATORY DATA ANALYSIS
# ============================================================================

print("\n" + "="*70)
print("📊 STEP 3: Exploratory Data Analysis")
print("="*70)

# Sales over time
print("\n📈 Generating sales trend visualization...")
daily_sales = df.groupby(date_col)[sales_col].sum().reset_index()

plt.figure(figsize=(14, 6))
plt.plot(daily_sales[date_col], daily_sales[sales_col], alpha=0.7, linewidth=2, color='#667eea')
plt.title('Sales Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Sales ($)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/sales_trend.png', dpi=300, bbox_inches='tight')
print("✅ Saved: visualizations/sales_trend.png")
plt.close()

# Monthly sales
print("\n📅 Generating monthly sales visualization...")
df['Year-Month'] = df[date_col].dt.to_period('M')
monthly_sales = df.groupby('Year-Month')[sales_col].sum()

plt.figure(figsize=(14, 6))
monthly_sales.plot(kind='line', marker='o', color='#667eea', linewidth=2)
plt.title('Monthly Sales Trend', fontsize=16, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/monthly_sales.png', dpi=300, bbox_inches='tight')
print("✅ Saved: visualizations/monthly_sales.png")
plt.close()

# ============================================================================
# STEP 4: FEATURE ENGINEERING
# ============================================================================

print("\n" + "="*70)
print("⚙️ STEP 4: Feature Engineering")
print("="*70)

print("\n🔧 Creating time-based features...")

# Aggregate to daily level
daily_data = df.groupby(date_col).agg({
    sales_col: 'sum'
}).reset_index()

daily_data.columns = ['date', 'sales']

# Create time-based features
daily_data['DayOfWeek'] = daily_data['date'].dt.dayofweek
daily_data['Month'] = daily_data['date'].dt.month
daily_data['Quarter'] = daily_data['date'].dt.quarter
daily_data['Year'] = daily_data['date'].dt.year
daily_data['DayOfYear'] = daily_data['date'].dt.dayofyear
daily_data['WeekOfYear'] = daily_data['date'].dt.isocalendar().week.astype(int)
daily_data['IsWeekend'] = (daily_data['DayOfWeek'] >= 5).astype(int)

print("✅ Created time features: DayOfWeek, Month, Quarter, Year, etc.")

# Create lag features
print("\n🔄 Creating lag features...")
for lag in [1, 7, 14, 30]:
    daily_data[f'Sales_Lag_{lag}'] = daily_data['sales'].shift(lag)

print("✅ Created lag features: 1, 7, 14, 30 days")

# Rolling averages
print("\n📊 Creating rolling averages...")
daily_data['Sales_MA_7'] = daily_data['sales'].rolling(window=7, min_periods=1).mean()
daily_data['Sales_MA_30'] = daily_data['sales'].rolling(window=30, min_periods=1).mean()

print("✅ Created moving averages: 7-day, 30-day")

# Drop rows with NaN
daily_data = daily_data.dropna()

print(f"\n✅ Feature engineering complete: {daily_data.shape[0]} rows, {daily_data.shape[1]} columns")

# ============================================================================
# STEP 5: PREPARE TRAINING DATA
# ============================================================================

print("\n" + "="*70)
print("🎯 STEP 5: Preparing Training Data")
print("="*70)

# Select features
feature_columns = [
    'DayOfWeek', 'Month', 'Quarter', 'Year', 'DayOfYear', 'WeekOfYear', 'IsWeekend',
    'Sales_Lag_1', 'Sales_Lag_7', 'Sales_Lag_14', 'Sales_Lag_30',
    'Sales_MA_7', 'Sales_MA_30'
]

X = daily_data[feature_columns]
y = daily_data['sales']

# Split data (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

print(f"\n✅ Training set: {X_train.shape[0]} samples")
print(f"✅ Test set: {X_test.shape[0]} samples")
print(f"✅ Features: {len(feature_columns)}")

# ============================================================================
# STEP 6: TRAIN LINEAR REGRESSION
# ============================================================================

print("\n" + "="*70)
print("🤖 STEP 6: Training Linear Regression Model")
print("="*70)

print("\n🔄 Training Linear Regression...")
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Predictions
lr_train_pred = lr_model.predict(X_train)
lr_test_pred = lr_model.predict(X_test)

# Evaluate
lr_metrics = {
    'train_mae': mean_absolute_error(y_train, lr_train_pred),
    'train_rmse': np.sqrt(mean_squared_error(y_train, lr_train_pred)),
    'train_r2': r2_score(y_train, lr_train_pred),
    'test_mae': mean_absolute_error(y_test, lr_test_pred),
    'test_rmse': np.sqrt(mean_squared_error(y_test, lr_test_pred)),
    'test_r2': r2_score(y_test, lr_test_pred)
}

print("\n✅ Linear Regression Performance:")
print(f"   Train MAE: ${lr_metrics['train_mae']:.2f}")
print(f"   Train RMSE: ${lr_metrics['train_rmse']:.2f}")
print(f"   Train R²: {lr_metrics['train_r2']:.4f}")
print(f"   Test MAE: ${lr_metrics['test_mae']:.2f}")
print(f"   Test RMSE: ${lr_metrics['test_rmse']:.2f}")
print(f"   Test R²: {lr_metrics['test_r2']:.4f}")

# ============================================================================
# STEP 7: TRAIN RANDOM FOREST
# ============================================================================

print("\n" + "="*70)
print("🌲 STEP 7: Training Random Forest Model")
print("="*70)

print("\n🔄 Training Random Forest (this may take a minute)...")
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1,
    verbose=0
)
rf_model.fit(X_train, y_train)

# Predictions
rf_train_pred = rf_model.predict(X_train)
rf_test_pred = rf_model.predict(X_test)

# Evaluate
rf_metrics = {
    'train_mae': mean_absolute_error(y_train, rf_train_pred),
    'train_rmse': np.sqrt(mean_squared_error(y_train, rf_train_pred)),
    'train_r2': r2_score(y_train, rf_train_pred),
    'test_mae': mean_absolute_error(y_test, rf_test_pred),
    'test_rmse': np.sqrt(mean_squared_error(y_test, rf_test_pred)),
    'test_r2': r2_score(y_test, rf_test_pred)
}

print("\n✅ Random Forest Performance:")
print(f"   Train MAE: ${rf_metrics['train_mae']:.2f}")
print(f"   Train RMSE: ${rf_metrics['train_rmse']:.2f}")
print(f"   Train R²: {rf_metrics['train_r2']:.4f}")
print(f"   Test MAE: ${rf_metrics['test_mae']:.2f}")
print(f"   Test RMSE: ${rf_metrics['test_rmse']:.2f}")
print(f"   Test R²: {rf_metrics['test_r2']:.4f}")

# ============================================================================
# STEP 8: MODEL COMPARISON
# ============================================================================

print("\n" + "="*70)
print("📊 STEP 8: Model Comparison")
print("="*70)

comparison = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest'],
    'Test MAE': [lr_metrics['test_mae'], rf_metrics['test_mae']],
    'Test RMSE': [lr_metrics['test_rmse'], rf_metrics['test_rmse']],
    'Test R²': [lr_metrics['test_r2'], rf_metrics['test_r2']]
})

print("\n" + comparison.to_string(index=False))

# Determine best model
best_model = 'Random Forest' if rf_metrics['test_mae'] < lr_metrics['test_mae'] else 'Linear Regression'
print(f"\n🏆 Best Model: {best_model}")

# Visualize comparison
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

metrics = ['Test MAE', 'Test RMSE', 'Test R²']
colors = ['#667eea', '#764ba2']

for idx, metric in enumerate(metrics):
    axes[idx].bar(comparison['Model'], comparison[metric], color=colors)
    axes[idx].set_title(metric, fontsize=14, fontweight='bold')
    axes[idx].set_ylabel('Value')
    axes[idx].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('visualizations/model_comparison.png', dpi=300, bbox_inches='tight')
print("\n✅ Saved: visualizations/model_comparison.png")
plt.close()

# ============================================================================
# STEP 9: VISUALIZE PREDICTIONS
# ============================================================================

print("\n" + "="*70)
print("📈 STEP 9: Visualizing Predictions")
print("="*70)

test_dates = daily_data.iloc[len(X_train):]['date'].values

plt.figure(figsize=(14, 6))
plt.plot(test_dates, y_test.values, label='Actual Sales', linewidth=2, color='black')
plt.plot(test_dates, lr_test_pred, label='Linear Regression', linewidth=2, alpha=0.7, color='#667eea')
plt.plot(test_dates, rf_test_pred, label='Random Forest', linewidth=2, alpha=0.7, color='#764ba2')
plt.title('Sales Forecast: Actual vs Predicted', fontsize=16, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Sales ($)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/forecast_comparison.png', dpi=300, bbox_inches='tight')
print("\n✅ Saved: visualizations/forecast_comparison.png")
plt.close()

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(feature_importance['Feature'], feature_importance['Importance'], color='#667eea')
plt.xlabel('Importance')
plt.title('Feature Importance (Random Forest)', fontsize=16, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('visualizations/feature_importance.png', dpi=300, bbox_inches='tight')
print("✅ Saved: visualizations/feature_importance.png")
plt.close()

# ============================================================================
# STEP 10: SAVE MODELS
# ============================================================================

print("\n" + "="*70)
print("💾 STEP 10: Saving Models")
print("="*70)

print("\n🔄 Saving models to backend/models/...")

# Save models
joblib.dump(lr_model, 'backend/models/linear_regression_model.pkl')
print("✅ Saved: backend/models/linear_regression_model.pkl")

joblib.dump(rf_model, 'backend/models/random_forest_model.pkl')
print("✅ Saved: backend/models/random_forest_model.pkl")

# Save feature columns
joblib.dump(feature_columns, 'backend/models/feature_columns.pkl')
print("✅ Saved: backend/models/feature_columns.pkl")

# Save metrics
metrics_summary = {
    'linear_regression': lr_metrics,
    'random_forest': rf_metrics,
    'best_model': best_model,
    'feature_columns': feature_columns,
    'training_date': datetime.now().isoformat()
}
joblib.dump(metrics_summary, 'backend/models/model_metrics.pkl')
print("✅ Saved: backend/models/model_metrics.pkl")

# ============================================================================
# STEP 11: BUSINESS INSIGHTS
# ============================================================================

print("\n" + "="*70)
print("💡 STEP 11: Business Insights & Recommendations")
print("="*70)

print("\n📊 KEY FINDINGS:")
print(f"   • Dataset: {df.shape[0]} transactions analyzed")
print(f"   • Date Range: {df[date_col].min().date()} to {df[date_col].max().date()}")
print(f"   • Average Daily Sales: ${daily_data['sales'].mean():.2f}")
print(f"   • Peak Sales Day: ${daily_data['sales'].max():.2f}")
print(f"   • Best Model: {best_model}")
print(f"   • Model Accuracy: {max(lr_metrics['test_r2'], rf_metrics['test_r2'])*100:.1f}%")
print(f"   • Prediction Error: ${min(lr_metrics['test_mae'], rf_metrics['test_mae']):.2f}")

print("\n🎯 TOP 3 IMPORTANT FEATURES:")
for idx, row in feature_importance.head(3).iterrows():
    print(f"   {idx+1}. {row['Feature']}: {row['Importance']:.4f}")

print("\n💼 BUSINESS RECOMMENDATIONS:")
print("   ✓ Use forecasts for inventory planning")
print("   ✓ Prepare for seasonal demand variations")
print("   ✓ Monitor prediction errors weekly")
print("   ✓ Update models monthly with new data")
print("   ✓ Set up alerts for unusual predictions")

print("\n🚀 NEXT STEPS:")
print("   1. Start backend: cd backend && python main.py")
print("   2. Start frontend: cd frontend && npm run dev")
print("   3. Upload your CSV and test predictions")
print("   4. Take screenshots for your submission")
print("   5. Post on LinkedIn with #FutureInterns")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*70)
print("🎉 TRAINING COMPLETE!")
print("="*70)

print("\n📁 Files Created:")
print("   backend/models/")
print("   ├── linear_regression_model.pkl")
print("   ├── random_forest_model.pkl")
print("   ├── feature_columns.pkl")
print("   └── model_metrics.pkl")
print("\n   visualizations/")
print("   ├── sales_trend.png")
print("   ├── monthly_sales.png")
print("   ├── model_comparison.png")
print("   ├── forecast_comparison.png")
print("   └── feature_importance.png")

print("\n✅ Your models are ready for deployment!")
print("✅ Run your backend and frontend to see them in action!")

print("\n" + "="*70)
