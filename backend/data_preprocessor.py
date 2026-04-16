"""
Robust Data Preprocessing Pipeline for Time Series Forecasting
Handles any dataset automatically with intelligent column detection
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Production-ready data preprocessing pipeline for time series forecasting.
    Automatically detects date and target columns, handles missing values,
    and prepares features for ML models.
    """
    
    def __init__(self, scaling_method: str = 'standard'):
        """
        Initialize preprocessor
        
        Args:
            scaling_method: 'standard' or 'minmax' for feature scaling
        """
        self.scaling_method = scaling_method
        self.scaler = StandardScaler() if scaling_method == 'standard' else MinMaxScaler()
        self.date_column = None
        self.target_column = None
        self.feature_columns = []
        
    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names: lowercase, strip spaces, replace spaces with underscores
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with standardized column names
        """
        logger.info("📝 Standardizing column names...")
        
        original_columns = df.columns.tolist()
        
        # Standardize: lowercase, strip, replace spaces and special chars
        df.columns = (
            df.columns
            .str.lower()
            .str.strip()
            .str.replace(' ', '_', regex=False)
            .str.replace('[^a-z0-9_]', '', regex=True)
        )
        
        logger.info(f"✅ Standardized {len(df.columns)} columns")
        for old, new in zip(original_columns, df.columns):
            if old != new:
                logger.info(f"   '{old}' → '{new}'")
        
        return df
    
    def detect_date_column(self, df: pd.DataFrame, manual_column: Optional[str] = None) -> str:
        """
        Automatically detect date column or use manual override
        
        Args:
            df: Input dataframe
            manual_column: Optional manual column name override
            
        Returns:
            Name of detected date column
            
        Raises:
            ValueError: If no valid date column found
        """
        logger.info("📅 Detecting date column...")
        
        # If manual column provided, validate it
        if manual_column:
            manual_column = manual_column.lower().strip().replace(' ', '_').replace('[^a-z0-9_]', '')
            if manual_column in df.columns:
                try:
                    pd.to_datetime(df[manual_column], errors='coerce')
                    logger.info(f"✅ Using manual date column: '{manual_column}'")
                    return manual_column
                except:
                    logger.warning(f"⚠️ Manual column '{manual_column}' is not a valid date column")
        
        # Auto-detect: try parsing each column
        date_candidates = []
        
        for col in df.columns:
            # Skip if column name doesn't suggest it's a date
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['date', 'time', 'day', 'month', 'year']):
                try:
                    parsed = pd.to_datetime(df[col], errors='coerce')
                    valid_ratio = parsed.notna().sum() / len(df)
                    
                    if valid_ratio > 0.5:  # At least 50% valid dates
                        date_candidates.append((col, valid_ratio))
                        logger.info(f"   Found date candidate: '{col}' ({valid_ratio*100:.1f}% valid)")
                except:
                    continue
        
        # If no candidates from name matching, try all columns
        if not date_candidates:
            logger.info("   No date columns found by name, trying all columns...")
            for col in df.columns:
                try:
                    parsed = pd.to_datetime(df[col], errors='coerce')
                    valid_ratio = parsed.notna().sum() / len(df)
                    
                    if valid_ratio > 0.8:  # Higher threshold for unnamed columns
                        date_candidates.append((col, valid_ratio))
                        logger.info(f"   Found date candidate: '{col}' ({valid_ratio*100:.1f}% valid)")
                except:
                    continue
        
        if not date_candidates:
            raise ValueError(
                "❌ No valid date column found. Please ensure your dataset has a date column. "
                f"Available columns: {', '.join(df.columns.tolist())}"
            )
        
        # Select best candidate (highest valid ratio)
        best_date_col = max(date_candidates, key=lambda x: x[1])[0]
        logger.info(f"✅ Auto-detected date column: '{best_date_col}'")
        
        return best_date_col
    
    def detect_target_column(self, df: pd.DataFrame, date_col: str, 
                            manual_column: Optional[str] = None) -> str:
        """
        Automatically detect target column (sales/revenue) or use manual override
        
        Args:
            df: Input dataframe
            date_col: Name of date column to exclude
            manual_column: Optional manual column name override
            
        Returns:
            Name of detected target column
            
        Raises:
            ValueError: If no valid numeric target column found
        """
        logger.info("💰 Detecting target column...")
        
        # If manual column provided, validate it
        if manual_column:
            manual_column = manual_column.lower().strip().replace(' ', '_').replace('[^a-z0-9_]', '')
            if manual_column in df.columns:
                if pd.api.types.is_numeric_dtype(df[manual_column]):
                    logger.info(f"✅ Using manual target column: '{manual_column}'")
                    return manual_column
                else:
                    logger.warning(f"⚠️ Manual column '{manual_column}' is not numeric")
        
        # Get numeric columns (exclude date column)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col != date_col]
        
        if not numeric_cols:
            raise ValueError(
                "❌ No numeric columns found for target. "
                f"Available columns: {', '.join(df.columns.tolist())}"
            )
        
        # Priority 1: Look for sales/revenue keywords
        target_keywords = ['sales', 'revenue', 'amount', 'total', 'value', 'price']
        for keyword in target_keywords:
            for col in numeric_cols:
                if keyword in col.lower():
                    logger.info(f"✅ Auto-detected target column by keyword: '{col}'")
                    return col
        
        # Priority 2: Select column with highest variance (most interesting)
        variances = {col: df[col].var() for col in numeric_cols}
        best_target = max(variances, key=variances.get)
        
        logger.info(f"✅ Auto-detected target column by variance: '{best_target}'")
        logger.info(f"   Other numeric columns: {', '.join([c for c in numeric_cols if c != best_target])}")
        
        return best_target
    
    def parse_dates(self, df: pd.DataFrame, date_col: str) -> pd.DataFrame:
        """
        Parse dates with multiple format support and error handling
        
        Args:
            df: Input dataframe
            date_col: Name of date column
            
        Returns:
            DataFrame with parsed dates
        """
        logger.info(f"🔄 Parsing dates in column '{date_col}'...")
        
        original_count = len(df)
        
        # Parse dates with coerce (invalid → NaT)
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Count invalid dates
        invalid_count = df[date_col].isna().sum()
        
        if invalid_count > 0:
            logger.warning(f"⚠️ Found {invalid_count} invalid dates, dropping them...")
            df = df.dropna(subset=[date_col])
        
        # Sort by date
        df = df.sort_values(date_col).reset_index(drop=True)
        
        logger.info(f"✅ Parsed dates: {len(df)}/{original_count} rows valid")
        logger.info(f"   Date range: {df[date_col].min()} to {df[date_col].max()}")
        
        return df
    
    def aggregate_by_date(self, df: pd.DataFrame, date_col: str, target_col: str) -> pd.DataFrame:
        """
        Aggregate data to daily level (one row per date)
        
        Args:
            df: Input dataframe
            date_col: Name of date column
            target_col: Name of target column
            
        Returns:
            Aggregated dataframe
        """
        logger.info("📊 Aggregating data by date...")
        
        original_count = len(df)
        
        # Prepare aggregation dictionary
        agg_dict = {target_col: 'sum'}
        
        # Add other numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numeric_cols:
            if col != target_col and col != date_col:
                agg_dict[col] = 'sum'
        
        # Aggregate
        df_agg = df.groupby(date_col).agg(agg_dict).reset_index()
        
        logger.info(f"✅ Aggregated: {original_count} rows → {len(df_agg)} unique dates")
        
        return df_agg
    
    def engineer_features(self, df: pd.DataFrame, date_col: str, target_col: str,
                         create_lags: bool = True, create_rolling: bool = True) -> pd.DataFrame:
        """
        Create time-based and lag features (matching pre-trained model format)
        
        Args:
            df: Input dataframe
            date_col: Name of date column
            target_col: Name of target column
            create_lags: Whether to create lag features
            create_rolling: Whether to create rolling mean features
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("⚙️ Engineering features...")
        
        # Time-based features (match model's expected names)
        df['Year'] = df[date_col].dt.year
        df['Month'] = df[date_col].dt.month
        df['DayOfWeek'] = df[date_col].dt.dayofweek
        df['Quarter'] = df[date_col].dt.quarter
        df['DayOfYear'] = df[date_col].dt.dayofyear
        df['WeekOfYear'] = df[date_col].dt.isocalendar().week.astype(int)
        df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
        
        logger.info("   ✓ Created time-based features: Year, Month, DayOfWeek, etc.")
        
        # Rename target to 'sales' for consistency
        if target_col != 'sales':
            df['sales'] = df[target_col]
        
        # Add quantity and profit if they don't exist (use sales as proxy)
        if 'quantity' not in df.columns:
            df['quantity'] = df['sales'] / df['sales'].mean()
        if 'profit' not in df.columns:
            df['profit'] = df['sales'] * 0.2  # Assume 20% profit margin
        
        # Lag features (match model's expected names)
        if create_lags:
            df['Sales_Lag_1'] = df['sales'].shift(1)
            df['Sales_Lag_7'] = df['sales'].shift(7)
            df['Sales_Lag_14'] = df['sales'].shift(14)
            df['Sales_Lag_30'] = df['sales'].shift(30)
            logger.info("   ✓ Created lag features: Sales_Lag_1, Sales_Lag_7, Sales_Lag_14, Sales_Lag_30")
        
        # Rolling mean features (match model's expected names)
        if create_rolling:
            df['Sales_MA_7'] = df['sales'].rolling(window=7, min_periods=1).mean()
            df['Sales_MA_30'] = df['sales'].rolling(window=30, min_periods=1).mean()
            logger.info("   ✓ Created rolling features: Sales_MA_7, Sales_MA_30")
        
        logger.info(f"✅ Feature engineering complete: {len(df.columns)} total columns")
        
        return df
    
    def handle_missing_values(self, df: pd.DataFrame, target_col: str) -> pd.DataFrame:
        """
        Handle missing values intelligently
        
        Args:
            df: Input dataframe
            target_col: Name of target column
            
        Returns:
            DataFrame with missing values handled
        """
        logger.info("🔧 Handling missing values...")
        
        original_count = len(df)
        missing_before = df.isnull().sum().sum()
        
        # Drop rows where target is missing
        df = df.dropna(subset=[target_col])
        
        # Fill numeric columns with median
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in numeric_cols:
            if col != target_col and df[col].isnull().any():
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                logger.info(f"   Filled '{col}' with median: {median_val:.2f}")
        
        missing_after = df.isnull().sum().sum()
        
        logger.info(f"✅ Missing values: {missing_before} → {missing_after}")
        logger.info(f"   Rows: {original_count} → {len(df)}")
        
        return df
    
    def scale_features(self, df: pd.DataFrame, date_col: str, target_col: str,
                      fit: bool = True) -> Tuple[pd.DataFrame, List[str]]:
        """
        Scale numeric features (NOT target column)
        
        Args:
            df: Input dataframe
            date_col: Name of date column to exclude
            target_col: Name of target column to exclude
            fit: Whether to fit the scaler (True for training, False for inference)
            
        Returns:
            Tuple of (scaled dataframe, list of scaled feature names)
        """
        logger.info(f"📏 Scaling features using {self.scaling_method}...")
        
        # Get numeric columns to scale (exclude date and target)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        cols_to_scale = [col for col in numeric_cols if col not in [date_col, target_col]]
        
        if not cols_to_scale:
            logger.info("   No features to scale")
            return df, []
        
        # Scale
        if fit:
            df[cols_to_scale] = self.scaler.fit_transform(df[cols_to_scale])
            logger.info(f"✅ Fitted and scaled {len(cols_to_scale)} features")
        else:
            df[cols_to_scale] = self.scaler.transform(df[cols_to_scale])
            logger.info(f"✅ Scaled {len(cols_to_scale)} features")
        
        return df, cols_to_scale
    
    def prepare_ml_data(self, df: pd.DataFrame, date_col: str, target_col: str) -> Dict[str, Any]:
        """
        Prepare final X (features) and y (target) for ML models
        
        Args:
            df: Preprocessed dataframe
            date_col: Name of date column
            target_col: Name of target column
            
        Returns:
            Dictionary with X, y, feature_names, and metadata
        """
        logger.info("🎯 Preparing ML data (X, y)...")
        
        # Exclude date column from features
        feature_cols = [col for col in df.columns if col not in [date_col, target_col]]
        
        X = df[feature_cols].values
        y = df[target_col].values
        
        logger.info(f"✅ X shape: {X.shape}, y shape: {y.shape}")
        logger.info(f"   Features: {', '.join(feature_cols[:10])}{'...' if len(feature_cols) > 10 else ''}")
        
        return {
            'X': X,
            'y': y,
            'feature_names': feature_cols,
            'dates': df[date_col].values,
            'n_samples': len(df),
            'n_features': len(feature_cols)
        }
    
    def process(self, df: pd.DataFrame, 
                date_column: Optional[str] = None,
                target_column: Optional[str] = None,
                create_lags: bool = True,
                create_rolling: bool = True,
                scale_features: bool = False) -> Dict[str, Any]:
        """
        Complete preprocessing pipeline
        
        Args:
            df: Input dataframe
            date_column: Optional manual date column name
            target_column: Optional manual target column name
            create_lags: Whether to create lag features
            create_rolling: Whether to create rolling features
            scale_features: Whether to scale features
            
        Returns:
            Dictionary with processed data and metadata
        """
        logger.info("="*70)
        logger.info("🚀 Starting Data Preprocessing Pipeline")
        logger.info("="*70)
        
        try:
            # Step 1: Standardize column names
            df = self.standardize_column_names(df)
            
            # Step 2: Detect date column
            self.date_column = self.detect_date_column(df, date_column)
            
            # Step 3: Detect target column
            self.target_column = self.detect_target_column(df, self.date_column, target_column)
            
            # Step 4: Parse dates
            df = self.parse_dates(df, self.date_column)
            
            # Step 5: Aggregate by date
            df = self.aggregate_by_date(df, self.date_column, self.target_column)
            
            # Step 6: Engineer features
            df = self.engineer_features(df, self.date_column, self.target_column, 
                                       create_lags, create_rolling)
            
            # Step 7: Handle missing values
            df = self.handle_missing_values(df, self.target_column)
            
            # Step 8: Scale features (optional)
            scaled_features = []
            if scale_features:
                df, scaled_features = self.scale_features(df, self.date_column, self.target_column)
            
            # Step 9: Prepare ML data
            ml_data = self.prepare_ml_data(df, self.date_column, self.target_column)
            
            logger.info("="*70)
            logger.info("✅ Preprocessing Complete!")
            logger.info("="*70)
            
            return {
                'dataframe': df,
                'date_column': self.date_column,
                'target_column': self.target_column,
                'X': ml_data['X'],
                'y': ml_data['y'],
                'feature_names': ml_data['feature_names'],
                'dates': ml_data['dates'],
                'n_samples': ml_data['n_samples'],
                'n_features': ml_data['n_features'],
                'scaled_features': scaled_features,
                'success': True,
                'message': 'Data preprocessing successful'
            }
            
        except Exception as e:
            logger.error(f"❌ Preprocessing failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Preprocessing failed: {str(e)}'
            }


# Convenience function for quick usage
def preprocess_data(df: pd.DataFrame, 
                   date_column: Optional[str] = None,
                   target_column: Optional[str] = None,
                   **kwargs) -> Dict[str, Any]:
    """
    Quick preprocessing function
    
    Args:
        df: Input dataframe
        date_column: Optional date column name
        target_column: Optional target column name
        **kwargs: Additional arguments for preprocessor
        
    Returns:
        Preprocessing results dictionary
    """
    preprocessor = DataPreprocessor()
    return preprocessor.process(df, date_column, target_column, **kwargs)
