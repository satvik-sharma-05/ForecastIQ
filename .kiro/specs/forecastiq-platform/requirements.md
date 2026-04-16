# Requirements Document

## Introduction

ForecastIQ is a professional SaaS-grade sales forecasting platform that combines machine learning predictions with a modern web interface. The system enables retail businesses, startup founders, operations teams, and analysts to predict future sales and demand using historical data, delivering actionable insights through a visually appealing dashboard. The platform uses React with Tailwind CSS for the frontend, FastAPI for the backend, MongoDB for data persistence, and scikit-learn for ML models (Linear Regression and Random Forest).

## Glossary

- **ForecastIQ_System**: The complete sales forecasting platform including frontend, backend, database, and ML components
- **User**: An authenticated person using the platform (retail business owner, analyst, operations team member, or startup founder)
- **Dataset**: A CSV file containing historical sales or demand data uploaded by a User
- **Forecast_Run**: A single execution of a prediction model on a Dataset, producing predictions and metrics
- **ML_Model**: A trained machine learning model (Linear Regression or Random Forest) used for predictions
- **Insight**: An automatically generated business recommendation based on forecast results (e.g., seasonality detection, peak periods)
- **Dashboard**: The main visualization interface displaying KPIs, charts, and insights
- **API_Backend**: The FastAPI server handling data processing, model execution, and database operations
- **Frontend**: The React-based user interface with Tailwind CSS styling
- **MongoDB_Database**: The database storing users, datasets, forecast runs, insights, and logs
- **CSV_File**: Comma-separated values file format for dataset uploads
- **JWT_Token**: JSON Web Token used for user authentication
- **KPI**: Key Performance Indicator (total sales, growth percentage, average sales)
- **MAE**: Mean Absolute Error - a model performance metric
- **RMSE**: Root Mean Square Error - a model performance metric
- **R²**: R-squared coefficient - a model performance metric
- **Feature_Engineering**: The process of creating date features, lag features, and rolling averages from raw data
- **Time_Series_Data**: Sequential data points indexed by time (dates)
- **Prediction_Confidence**: The statistical confidence interval around forecast predictions
- **Google_Colab**: External platform for training ML models (not performed locally)
- **Report**: An exported document (CSV or PDF) containing forecast results, graphs, and insights

## Requirements

### Requirement 1: User Authentication and Account Management

**User Story:** As a User, I want to create an account and log in securely, so that I can access my personalized forecasting dashboard and saved data.

#### Acceptance Criteria

1. THE ForecastIQ_System SHALL provide a registration endpoint accepting email, password, and name
2. WHEN a User submits valid registration credentials, THE API_Backend SHALL create a new user account in the MongoDB_Database
3. WHEN a User submits duplicate email credentials, THE API_Backend SHALL return an error message indicating the email is already registered
4. THE ForecastIQ_System SHALL provide a login endpoint accepting email and password
5. WHEN a User submits valid login credentials, THE API_Backend SHALL return a JWT_Token with 1440 minute expiration
6. WHEN a User submits invalid login credentials, THE API_Backend SHALL return an authentication error
7. THE Frontend SHALL store the JWT_Token securely for subsequent API requests
8. WHEN a JWT_Token expires, THE API_Backend SHALL return an unauthorized error requiring re-authentication

### Requirement 2: Dataset Upload and Validation

**User Story:** As a User, I want to u