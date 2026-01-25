
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# ==========================================
# CONFIGURATION
# ==========================================
# Robust path resolution
script_dir = os.path.dirname(os.path.abspath(__file__))
# Input: CleanedDataset.csv is in the sibling folder "DataCleaning"
input_path = os.path.join(script_dir, "..", "DataCleaning", "CleanedDataset.csv")
output_path = os.path.join(script_dir, "FeatureEngineeredDataset.csv")

input_path = os.path.abspath(input_path)
output_path = os.path.abspath(output_path)

print("--- Starting Feature Engineering Pipeline ---")

# ==========================================
# 1. LOAD DATA
# ==========================================
if not os.path.exists(input_path):
    print(f"Error: Input file not found at {input_path}")
    print("Please run DataCleaning.py first.")
    exit()

print(f"Loading data from {input_path}...")
df = pd.read_csv(input_path)
print(f"Initial Shape: {df.shape}")

# Ensure timestamp is datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# ==========================================
# 2. FEATURE EXTRACTION (TIME)
# ==========================================
print("Extracting Time Features...")
df['hour_of_day'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek # 0=Monday, 6=Sunday
df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

# ==========================================
# 3. DERIVED FEATURES (INTERACTIONS)
# ==========================================
print("Creating Derived Features...")

# Data Intensity (MB per minute)
# Avoid division by zero: max(duration, 1)
df['data_intensity'] = df['data_download_mb'] / df['session_duration'].replace(0, 1)

# Access Rate (Accesses per minute)
df['access_rate'] = df['access_count'] / df['session_duration'].replace(0, 1)

# ==========================================
# 4. CATEGORICAL ENCODING
# ==========================================
print("Encoding Categorical Variables...")

# Label Encode Role
# We use LabelEncoder for simplicity. OneHot might be better for some models, 
# but for Tree-based models (Isolation Forest/XGBoost), Label works fine.
le_role = LabelEncoder()
df['role_encoded'] = le_role.fit_transform(df['role'].astype(str))
print(f"  - Roles Encoded: {dict(zip(le_role.classes_, le_role.transform(le_role.classes_)))}")

# Target Generation
# 'is_attack' = 1 if attack_type is NOT 'Normal'
df['is_attack'] = df['attack_type'].apply(lambda x: 0 if x == 'Normal' else 1)

# Encode Attack Type for Multi-class classification
le_attack = LabelEncoder()
df['attack_class'] = le_attack.fit_transform(df['attack_type'].astype(str))
print(f"  - Attacks Encoded: {dict(zip(le_attack.classes_, le_attack.transform(le_attack.classes_)))}")

# ==========================================
# 5. SELECT & DROP COLUMNS
# ==========================================
print("Selecting Final Features...")

# Columns to Drop (Not needed for ML)
cols_to_drop = ['timestamp', 'user_id', 'role', 'attack_type']
df_ml = df.drop(columns=cols_to_drop)

# Handle potential Infinite values from division
df_ml.replace([np.inf, -np.inf], 0, inplace=True)
df_ml.fillna(0, inplace=True)

# ==========================================
# 6. SCALING (NORMALIZATION)
# ==========================================
print("Scaling Numerical Features (MinMax)...")

# Features to Scale
scale_cols = [
    'session_duration', 'data_download_mb', 'transaction_amount', 
    'access_count', 'data_intensity', 'access_rate', 
    'login_frequency', 'login_hour', 'failed_logins'
]

scaler = MinMaxScaler()
# Only scale columns that exist
existing_scale_cols = [c for c in scale_cols if c in df_ml.columns]

if existing_scale_cols:
    df_ml[existing_scale_cols] = scaler.fit_transform(df_ml[existing_scale_cols])

# ==========================================
# 7. SAVE OUTPUT
# ==========================================
print(f"Final Shape: {df_ml.shape}")
print(f"Saving to {output_path}...")
df_ml.to_csv(output_path, index=False)
print("Done!")

# Preview
print("\nFeature Engineered Data Preview:")
print(df_ml.head())
print("\nColumns:")
print(list(df_ml.columns))
