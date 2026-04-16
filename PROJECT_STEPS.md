# ForecastIQ - Complete Project Implementation Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Step-by-Step Implementation](#step-by-step-implementation)
4. [Features Breakdown](#features-breakdown)
5. [Testing Guide](#testing-guide)
6. [Deployment](#deployment)

---

## 🎯 Project Overview

**ForecastIQ** is a full-stack ML-powered forecasting platform that enables users to:
- Upload historical sales/revenue datasets (CSV)
- Run machine learning forecasts using pre-trained models
- Compare model performance
- Get AI-generated business insights
- Track forecast history

**Tech Stack:**
- **Frontend:** React 18 + Vite, Tailwind CSS 3.4.1, Recharts, Lucide Icons
- **Backend:** FastAPI (Python), Motor (async MongoDB driver)
- **Database:** MongoDB Atlas
- **ML:** Scikit-learn (Linear Regression, Random Forest)
- **Auth:** JWT with bcrypt

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  React + Vite + Tailwind CSS + Recharts                     │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │  Home    │ Datasets │ Forecast │ Insights │ Compare  │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│                          ↓ HTTP/REST                         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                               │
│  FastAPI + JWT Auth + CORS                                  │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │   Auth   │ Datasets │ Forecast │ Insights │Dashboard │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ML Engine (Scikit-learn)                           │   │
│  │  - Data Preprocessing                               │   │
│  │  - Feature Engineering                              │   │
│  │  - Pre-trained Models (Linear Regression, RF)      │   │
│  │  - Insight Generation                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE (MongoDB)                        │
│  Collections: users, datasets, forecast_runs, insights      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Step-by-Step Implementation

### **PHASE 1: Backend Setup (Days 1-2)**

#### Step 1.1: Initialize Backend Structure
```bash
mkdir backend
cd backend
touch main.py models.py auth.py database.py config.py
touch requirements.txt .env
```

#### Step 1.2: Install Dependencies
```bash
pip install fastapi uvicorn motor pymongo python-jose[cryptography] passlib[bcrypt] python-multipart pandas scikit-learn numpy python-dotenv
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn==0.24.0
motor==3.3.2
pymongo==4.6.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pandas==2.1.3
scikit-learn==1.4.0
numpy==1.26.2
python-dotenv==1.0.0
```

#### Step 1.3: Configure Environment Variables
**backend/.env:**
```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0
MONGO_DB_NAME=forecastiq
SECRET_KEY=your-secret-key-here-min-32-chars
```

#### Step 1.4: Create Database Connection (database.py)
```python
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("❌ Closed MongoDB connection")

def get_database():
    return db
```

#### Step 1.5: Create Pydantic Models (models.py)
Define data models for:
- UserCreate, UserLogin, User
- Dataset, ForecastRun, Insight
- ForecastRequest, CompareRequest

#### Step 1.6: Implement JWT Authentication (auth.py)
```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

#### Step 1.7: Create FastAPI App (main.py)
- Set up CORS middleware
- Create auth routes (signup, login, me)
- Create dataset routes (upload, list, delete)
- Create forecast routes (run, history, details, compare)
- Create insights route
- Create dashboard stats route

---

### **PHASE 2: ML Engine Development (Days 3-4)**

#### Step 2.1: Create Data Preprocessor (data_preprocessor.py)
**Key Features:**
- Column name standardization (lowercase, remove spaces)
- Automatic date column detection
- Automatic target column detection
- Mixed date format handling
- Time series aggregation
- Feature engineering (lag features, rolling means, time features)
- Missing value handling

**Core Methods:**
```python
class DataPreprocessor:
    def standardize_column_names(df)
    def detect_date_column(df)
    def detect_target_column(df)
    def parse_dates(df, date_col)
    def aggregate_by_date(df, date_col, target_col)
    def engineer_features(df, target_col)
    def handle_missing_values(df, target_col)
    def process(df, date_col, target_col)
```

#### Step 2.2: Train ML Models (train_models.py)
```python
# Download datasets (Kaggle/UCI)
# Preprocess data
# Train Linear Regression
# Train Random Forest
# Save models as .pkl files
# Save feature columns and metrics
```

**Run training:**
```bash
python train_models.py
```

**Output:**
- `backend/models/linear_regression_model.pkl`
- `backend/models/random_forest_model.pkl`
- `backend/models/feature_columns.pkl`
- `backend/models/model_metrics.pkl`

#### Step 2.3: Create Pre-trained ML Engine (ml_engine_pretrained.py)
```python
class PretrainedForecastEngine:
    def __init__(self):
        # Load pre-trained models
        self.lr_model = joblib.load('models/linear_regression_model.pkl')
        self.rf_model = joblib.load('models/random_forest_model.pkl')
        self.feature_columns = joblib.load('models/feature_columns.pkl')
    
    def predict_with_pretrained(df, date_col, target_col, model_type, days):
        # Preprocess data
        # Ensure all features exist
        # Generate predictions
        # Calculate metrics
        return results
    
    def generate_insights(df, target_col, predictions):
        # Peak detection
        # Trend analysis
        # Future demand predictions
        return insights
```

---

### **PHASE 3: Frontend Setup (Days 5-6)**

#### Step 3.1: Initialize React App
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

#### Step 3.2: Install Dependencies
```bash
npm install react-router-dom axios recharts lucide-react
npm install -D tailwindcss@3.4.1 postcss autoprefixer
npx tailwindcss init -p
```

#### Step 3.3: Configure Tailwind CSS
**tailwind.config.js:**
```javascript
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
}
```

**postcss.config.js:**
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

#### Step 3.4: Create Axios Instance (src/api/axios.js)
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

#### Step 3.5: Create Reusable Components
- **EmptyState.jsx** - Empty state UI
- **Toast.jsx** - Toast notifications
- **LoadingSkeleton.jsx** - Loading placeholders
- **InsightCard.jsx** - Enhanced insight cards
- **HowToUse.jsx** - User guide panel
- **Layout.jsx** - App layout with sidebar

#### Step 3.6: Create Custom Hooks
- **useToast.js** - Toast notification management

#### Step 3.7: Add CSS Animations (src/index.css)
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(100px); }
  to { opacity: 1; transform: translateX(0); }
}
```

---

### **PHASE 4: Page Implementation (Days 7-9)**

#### Step 4.1: Create Home Page (Home.jsx)
- Hero section with CTA
- Feature cards (4 features)
- How it works (4 steps)
- Tech stack showcase
- Footer

#### Step 4.2: Create Auth Pages
- **Login.jsx** - Email/password login
- **Signup.jsx** - User registration

#### Step 4.3: Create Dashboard (Dashboard.jsx)
- Stats cards (datasets, forecasts, insights)
- Recent activity list
- Empty states when no data

#### Step 4.4: Create Datasets Page (Datasets.jsx)
- Upload CSV button
- Dataset cards with metadata
- Delete functionality
- Toast notifications
- Empty state

#### Step 4.5: Create Forecast Page (Forecast.jsx)
- Configuration panel (dataset, columns, model, days)
- How to Use guide
- Results panel (metrics, chart, insights)
- Loading skeletons
- Empty state

#### Step 4.6: Create History Page (History.jsx)
- List of past forecast runs
- Metrics display
- Loading skeletons
- Empty state

#### Step 4.7: Create Insights Page (Insights.jsx)
- Animated insight cards
- Icon-based categorization
- Loading skeletons
- Empty state

#### Step 4.8: Create Compare Page (Compare.jsx)
- Forecast selection panel
- Best model highlight
- Performance comparison chart
- Detailed metrics
- Empty state

---

### **PHASE 5: Integration & Testing (Days 10-11)**

#### Step 5.1: Backend Testing
```bash
cd backend
python test_api.py
```

Test endpoints:
- ✅ Signup
- ✅ Login
- ✅ Upload dataset
- ✅ Run forecast
- ✅ Get insights
- ✅ Compare forecasts

#### Step 5.2: Frontend Testing
- Test all page routes
- Test authentication flow
- Test dataset upload
- Test forecast generation
- Test model comparison
- Test error handling

#### Step 5.3: End-to-End Testing
1. Sign up new user
2. Upload sample dataset
3. Run forecast with both models
4. View insights
5. Compare forecasts
6. Check history

---

### **PHASE 6: Production Enhancements (Days 12-13)**

#### Step 6.1: Error Handling
- Backend: HTTPException with detailed messages
- Frontend: Toast notifications instead of alerts
- Validation: Column detection, date parsing

#### Step 6.2: UX Improvements
- Loading states everywhere
- Empty states with helpful messages
- Smooth animations
- Responsive design

#### Step 6.3: Performance Optimization
- Async database operations
- Efficient data preprocessing
- Model caching
- Frontend code splitting

---

## 🎨 Features Breakdown

### 1. Authentication System
**Backend:**
- JWT token generation
- Password hashing with bcrypt
- Token validation middleware

**Frontend:**
- Login/Signup forms
- Token storage in localStorage
- Protected routes
- Auto-redirect

### 2. Dataset Management
**Backend:**
- CSV file upload with encoding fallback
- Metadata extraction (columns, row count)
- File storage in uploads/ directory
- User-specific dataset isolation

**Frontend:**
- Drag-and-drop upload
- Dataset cards with preview
- Delete confirmation
- Toast notifications

### 3. ML Forecasting Engine
**Preprocessing:**
- Column standardization
- Auto-detection (date, target)
- Feature engineering (15 features)
- Missing value handling

**Models:**
- Linear Regression (fast, interpretable)
- Random Forest (accurate, robust)

**Features Generated:**
- Time features: DayOfWeek, Month, Quarter, Year, DayOfYear, WeekOfYear, IsWeekend
- Lag features: Sales_Lag_1, Sales_Lag_7, Sales_Lag_14, Sales_Lag_30
- Rolling features: Sales_MA_7, Sales_MA_30
- Additional: quantity, profit

### 4. Insights Generation
**Types:**
- **Peak:** High demand periods
- **Low:** Low demand periods
- **Trend:** Increasing/decreasing patterns
- **Forecast:** Future predictions

**Algorithm:**
- Statistical analysis (mean, std)
- Threshold-based detection
- Trend calculation

### 5. Model Comparison
**Metrics:**
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)

**Visualization:**
- Bar chart comparison
- Best model highlight
- Detailed metrics table

---

## 🧪 Testing Guide

### Backend Tests
```bash
cd backend
python test_api.py
python test_preprocessor.py
```

### Frontend Manual Tests
1. **Authentication:**
   - Sign up with new email
   - Login with credentials
   - Logout and verify redirect

2. **Dataset Upload:**
   - Upload valid CSV
   - Upload invalid file (should fail gracefully)
   - Delete dataset

3. **Forecast:**
   - Select dataset
   - Choose columns
   - Run forecast
   - View results

4. **Insights:**
   - Check insights page
   - Verify insight cards

5. **Compare:**
   - Select 2+ forecasts
   - Compare models
   - View best model

### Sample Test Data
Use `sample_sales_data.csv` or any CSV with:
- Date column (e.g., "Order Date", "Date")
- Numeric target (e.g., "Sales", "Revenue")

---

## 🚀 Deployment

### Backend Deployment (Render/Railway)
1. Create `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. Set environment variables:
   - MONGO_URI
   - MONGO_DB_NAME
   - SECRET_KEY

3. Deploy

### Frontend Deployment (Vercel/Netlify)
1. Update API base URL in `axios.js`
2. Build: `npm run build`
3. Deploy `dist/` folder

### Database (MongoDB Atlas)
1. Create cluster
2. Whitelist IP addresses
3. Create database user
4. Get connection string

---

## 📊 Project Statistics

- **Total Files:** 40+
- **Lines of Code:** ~5,000+
- **Components:** 15+
- **API Endpoints:** 15
- **Database Collections:** 4
- **ML Models:** 2
- **Features Engineered:** 15

---

## 🎓 Key Learnings

1. **Full-Stack Integration:** Connecting React frontend with FastAPI backend
2. **Async Programming:** Using Motor for async MongoDB operations
3. **ML Pipeline:** Data preprocessing → Training → Inference
4. **JWT Authentication:** Secure user authentication
5. **UX Design:** Empty states, loading states, error handling
6. **Production Practices:** Error handling, validation, testing

---

## 📚 Resources

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **Tailwind CSS:** https://tailwindcss.com/
- **Scikit-learn:** https://scikit-learn.org/
- **MongoDB:** https://www.mongodb.com/docs/

---

## 🏆 Resume Description

> Developed ForecastIQ, a full-stack ML-powered forecasting platform using React, FastAPI, MongoDB, and Scikit-learn. Implemented JWT authentication, async database operations, automated data preprocessing pipeline, pre-trained ML models (Linear Regression, Random Forest), and AI-generated business insights. Built production-ready UI with Tailwind CSS featuring empty states, loading skeletons, toast notifications, and interactive charts. Achieved 15+ API endpoints, 4 database collections, and 15 engineered features for accurate time-series predictions.

---

**Built with ❤️ by [Your Name]**
