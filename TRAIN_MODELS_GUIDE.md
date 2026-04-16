# 🚀 Quick Model Training Guide

## One-Command Training

Run this single Python script to:
- ✅ Download datasets automatically
- ✅ Train both Linear Regression and Random Forest
- ✅ Generate visualizations
- ✅ Save .pkl files ready for deployment

---

## Step 1: Install Dependencies

```bash
pip install -r training_requirements.txt
```

---

## Step 2: Run Training Script

```bash
python train_models.py
```

That's it! The script will:
1. Try to download Kaggle Superstore dataset
2. If that fails, try UCI Online Retail dataset
3. If that fails, use your sample_sales_data.csv
4. Clean and prepare the data
5. Create time-based features
6. Train both models
7. Evaluate performance
8. Generate visualizations
9. Save .pkl files to `backend/models/`

---

## What You'll Get

### Models (in `backend/models/`)
- `linear_regression_model.pkl` - Trained Linear Regression
- `random_forest_model.pkl` - Trained Random Forest
- `feature_columns.pkl` - Feature names for inference
- `model_metrics.pkl` - Performance metrics

### Visualizations (in `visualizations/`)
- `sales_trend.png` - Sales over time
- `monthly_sales.png` - Monthly aggregation
- `model_comparison.png` - Model performance comparison
- `forecast_comparison.png` - Actual vs Predicted
- `feature_importance.png` - Most important features

---

## Expected Output

```
🚀 ForecastIQ - Automated Model Training
======================================================================

📁 Directories created successfully!

======================================================================
📥 STEP 1: Downloading Datasets
======================================================================

🔄 Attempting to download Superstore dataset from Kaggle...
✅ Superstore dataset downloaded successfully!

✅ Dataset loaded: 9994 rows, 21 columns

======================================================================
🔍 STEP 2: Data Exploration & Cleaning
======================================================================

📅 Detected date columns: ['Order Date', 'Ship Date']
💰 Detected sales columns: ['Sales']

✅ Using: Date='Order Date', Sales='Sales'

🧹 Cleaning data...
✅ Cleaned dataset: 9994 rows
📅 Date range: 2014-01-03 to 2017-12-30

======================================================================
📊 STEP 3: Exploratory Data Analysis
======================================================================

📈 Generating sales trend visualization...
✅ Saved: visualizations/sales_trend.png

📅 Generating monthly sales visualization...
✅ Saved: visualizations/monthly_sales.png

======================================================================
⚙️ STEP 4: Feature Engineering
======================================================================

🔧 Creating time-based features...
✅ Created time features: DayOfWeek, Month, Quarter, Year, etc.

🔄 Creating lag features...
✅ Created lag features: 1, 7, 14, 30 days

📊 Creating rolling averages...
✅ Created moving averages: 7-day, 30-day

✅ Feature engineering complete: 1403 rows, 20 columns

======================================================================
🎯 STEP 5: Preparing Training Data
======================================================================

✅ Training set: 1122 samples
✅ Test set: 281 samples
✅ Features: 13

======================================================================
🤖 STEP 6: Training Linear Regression Model
======================================================================

🔄 Training Linear Regression...

✅ Linear Regression Performance:
   Train MAE: $1234.56
   Train RMSE: $1567.89
   Train R²: 0.8523
   Test MAE: $1345.67
   Test RMSE: $1678.90
   Test R²: 0.8412

======================================================================
🌲 STEP 7: Training Random Forest Model
======================================================================

🔄 Training Random Forest (this may take a minute)...

✅ Random Forest Performance:
   Train MAE: $987.65
   Train RMSE: $1234.56
   Train R²: 0.9234
   Test MAE: $1123.45
   Test RMSE: $1456.78
   Test R²: 0.9012

======================================================================
📊 STEP 8: Model Comparison
======================================================================

            Model  Test MAE  Test RMSE   Test R²
Linear Regression   1345.67    1678.90  0.841200
    Random Forest   1123.45    1456.78  0.901200

🏆 Best Model: Random Forest

✅ Saved: visualizations/model_comparison.png

======================================================================
📈 STEP 9: Visualizing Predictions
======================================================================

✅ Saved: visualizations/forecast_comparison.png
✅ Saved: visualizations/feature_importance.png

======================================================================
💾 STEP 10: Saving Models
======================================================================

🔄 Saving models to backend/models/...
✅ Saved: backend/models/linear_regression_model.pkl
✅ Saved: backend/models/random_forest_model.pkl
✅ Saved: backend/models/feature_columns.pkl
✅ Saved: backend/models/model_metrics.pkl

======================================================================
💡 STEP 11: Business Insights & Recommendations
======================================================================

📊 KEY FINDINGS:
   • Dataset: 9994 transactions analyzed
   • Date Range: 2014-01-03 to 2017-12-30
   • Average Daily Sales: $2297.20
   • Peak Sales Day: $22638.48
   • Best Model: Random Forest
   • Model Accuracy: 90.1%
   • Prediction Error: $1123.45

🎯 TOP 3 IMPORTANT FEATURES:
   1. Sales_Lag_1: 0.4523
   2. Sales_MA_7: 0.2341
   3. Sales_Lag_7: 0.1234

💼 BUSINESS RECOMMENDATIONS:
   ✓ Use forecasts for inventory planning
   ✓ Prepare for seasonal demand variations
   ✓ Monitor prediction errors weekly
   ✓ Update models monthly with new data
   ✓ Set up alerts for unusual predictions

🚀 NEXT STEPS:
   1. Start backend: cd backend && python main.py
   2. Start frontend: cd frontend && npm run dev
   3. Upload your CSV and test predictions
   4. Take screenshots for your submission
   5. Post on LinkedIn with #FutureInterns

======================================================================
🎉 TRAINING COMPLETE!
======================================================================

📁 Files Created:
   backend/models/
   ├── linear_regression_model.pkl
   ├── random_forest_model.pkl
   ├── feature_columns.pkl
   └── model_metrics.pkl

   visualizations/
   ├── sales_trend.png
   ├── monthly_sales.png
   ├── model_comparison.png
   ├── forecast_comparison.png
   └── feature_importance.png

✅ Your models are ready for deployment!
✅ Run your backend and frontend to see them in action!

======================================================================
```

---

## Troubleshooting

### If Kaggle download fails:
1. Set up Kaggle API: https://www.kaggle.com/docs/api
2. Download `kaggle.json` and place in `~/.kaggle/`
3. Or the script will automatically try UCI dataset

### If UCI download fails:
- The script will use `sample_sales_data.csv` automatically

### If everything fails:
- Make sure `sample_sales_data.csv` exists in the root directory
- Check internet connection
- Install missing packages: `pip install -r training_requirements.txt`

---

## After Training

Once training is complete:

1. **Start Backend**
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test the App**
   - Go to http://localhost:5173
   - Sign up / Login
   - Upload a CSV file
   - Run forecasts
   - View insights

4. **Take Screenshots**
   - Dashboard
   - Forecast results
   - Model comparison
   - Insights page

5. **Submit to Future Interns**
   - Include visualizations from `visualizations/` folder
   - Include model metrics
   - Explain your approach
   - Post on LinkedIn

---

## Time Required

- Dataset download: 1-2 minutes
- Model training: 2-3 minutes
- Total: ~5 minutes

---

## Questions?

Check `PROJECT_WORKFLOW.md` for detailed explanations!
