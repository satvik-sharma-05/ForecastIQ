"""
Test script for the robust data preprocessor
"""

import pandas as pd
from data_preprocessor import preprocess_data

# Test with sample data
print("="*70)
print("Testing Data Preprocessor")
print("="*70)

# Create test dataframe
test_data = {
    'Order Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
    'Sales Amount': [100, 150, 120, 180],
    'Quantity': [5, 7, 6, 9],
    'Region': ['North', 'South', 'East', 'West']
}

df = pd.DataFrame(test_data)

print("\nOriginal DataFrame:")
print(df)

# Test preprocessing
result = preprocess_data(df)

if result['success']:
    print("\n✅ Preprocessing successful!")
    print(f"Date column detected: {result['date_column']}")
    print(f"Target column detected: {result['target_column']}")
    print(f"Features created: {result['n_features']}")
    print(f"Samples: {result['n_samples']}")
    print(f"\nFeature names: {result['feature_names'][:10]}")
else:
    print(f"\n❌ Preprocessing failed: {result['error']}")
