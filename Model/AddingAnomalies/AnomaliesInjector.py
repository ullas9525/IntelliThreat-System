
import pandas as pd
import numpy as np
import random
import os

# ==========================================
# CONFIGURATION
# ==========================================
# Define paths relative to this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "..", "RawDataGeneration", "RawDataset.csv")
output_path = os.path.join(script_dir, "AnomalyDataset.csv")

# Resolve absolute paths to avoid confusion
input_path = os.path.abspath(input_path)
output_path = os.path.abspath(output_path)

# ==========================================
# 1. LOAD DATASET
# ==========================================
print("--- Starting Data Corruption Process ---")

# Check if input file exists
if not os.path.exists(input_path):
    print(f"Error: Input file not found at {input_path}")
    print("Please run RawData.py first.")
    exit()

print(f"Loading data from {input_path}...")
df = pd.read_csv(input_path)
print(f"Original Shape: {df.shape}")

# Create a copy to corrupt
df_corrupt = df.copy()

# Total rows
n_rows = len(df_corrupt)
# 10-15% of rows to be affected broadly (approx 12%)
n_affect = int(n_rows * 0.12)
indices = df_corrupt.index.tolist()

# ==========================================
# 2. INTRODUCE MISSING VALUES (NaN)
# ==========================================
print("Injecting Missing Values (NaN)...")
# Randomly select rows for missing values
missing_indices = random.sample(indices, int(n_rows * 0.05)) # 5% missing

# Numeric Column Nulls
df_corrupt.loc[missing_indices[:len(missing_indices)//2], 'transaction_amount'] = np.nan
df_corrupt.loc[missing_indices[len(missing_indices)//2:], 'data_download_mb'] = np.nan

# Categorical Column Nulls
cat_missing_indices = random.sample(indices, int(n_rows * 0.03)) # 3% missing
df_corrupt.loc[cat_missing_indices, 'role'] = np.nan

# ==========================================
# 3. INTRODUCE INVALID FORMATS (Dirty Strings)
# ==========================================
print("Injecting Invalid Formats (Strings in Numeric)...")
# Inject strings into numeric columns (e.g., 'Error', 'Unknown')
invalid_indices = random.sample(indices, int(n_rows * 0.02)) # 2% bad formats

for idx in invalid_indices:
    if random.random() > 0.5:
        df_corrupt.at[idx, 'session_duration'] = "Invalid_Time"
    else:
        df_corrupt.at[idx, 'risk_score'] = "High_Risk" # String in float column

# Malformed Timestamps
timestamp_indices = random.sample(indices, int(n_rows * 0.01))
for idx in timestamp_indices:
    df_corrupt.at[idx, 'timestamp'] = "24-24-2025" # Bad format

# ==========================================
# 4. INTRODUCE NEGATIVE VALUES (Logic Errors)
# ==========================================
print("Injecting Negative Values (Logical Errors)...")
negative_indices = random.sample(indices, int(n_rows * 0.02))

for idx in negative_indices:
    val = df_corrupt.at[idx, 'data_download_mb']
    if isinstance(val, (int, float)) and not pd.isna(val):
        df_corrupt.at[idx, 'data_download_mb'] = abs(val) * -1 # Make negative

# ==========================================
# 5. INTRODUCE EXTREME OUTLIERS (Statistical Noise)
# ==========================================
print("Injecting Extreme Outliers...")
outlier_indices = random.sample(indices, int(n_rows * 0.01))

for idx in outlier_indices:
    # 1 Billion amount (unrealistic even for fraud)
    df_corrupt.at[idx, 'transaction_amount'] = 999999999 
    # Impossible download size
    df_corrupt.at[idx, 'data_download_mb'] = 1000000 

# ==========================================
# 6. INCONSISTENT CATEGORICAL VALUES
# ==========================================
print("Injecting Inconsistent Categories (Typos/Case)...")
typo_indices = random.sample(indices, int(n_rows * 0.05))

for idx in typo_indices:
    role_val = str(df_corrupt.at[idx, 'role'])
    if role_val.lower() == 'admin':
        choices = ['ADMIN', 'admin ', 'Admn'] # Variations
        df_corrupt.at[idx, 'role'] = random.choice(choices)
    elif role_val.lower() == 'employee':
        df_corrupt.at[idx, 'role'] = 'empl'

# ==========================================
# 7. INTRODUCE DUPLICATE ROWS
# ==========================================
print("Injecting Duplicate Rows...")
# Select 100 random rows to duplicate
rows_to_dup = df_corrupt.sample(n=100)
df_corrupt = pd.concat([df_corrupt, rows_to_dup], ignore_index=True)

# ==========================================
# 8. SAVE CORRUPTED DATASET
# ==========================================
print(f"Final Shape: {df_corrupt.shape}")
print(f"Saving to {output_path}...")
df_corrupt.to_csv(output_path, index=False)
print("Done!")

# Preview
print("\nSample of Corrupted Data (NaNs and Typos):")
print(df_corrupt[df_corrupt.isnull().any(axis=1)].head(3))
