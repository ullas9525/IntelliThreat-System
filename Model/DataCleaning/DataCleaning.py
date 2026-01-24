
import pandas as pd
import numpy as np
import os

# ==========================================
# CONFIGURATION
# ==========================================
# Robust path resolution
script_dir = os.path.dirname(os.path.abspath(__file__))
# Input: AnomalyDataset.csv is in the sibling folder "AddingAnomalies"
input_path = os.path.join(script_dir, "..", "AddingAnomalies", "AnomalyDataset.csv")
output_path = os.path.join(script_dir, "CleanedDataset.csv")

input_path = os.path.abspath(input_path)
output_path = os.path.abspath(output_path)

print("--- Starting Data Cleaning Pipeline ---")

# ==========================================
# 1. LOAD DATA
# ==========================================
if not os.path.exists(input_path):
    print(f"Error: Input file not found at {input_path}")
    exit()

print(f"Loading data from {input_path}...")
df = pd.read_csv(input_path)
initial_rows = len(df)
print(f"Initial Shape: {df.shape}")

# ==========================================
# 2. REMOVE DUPLICATES
# ==========================================
duplicates = df.duplicated().sum()
if duplicates > 0:
    print(f"Detected {duplicates} duplicate rows. Removing...")
    df.drop_duplicates(inplace=True)
else:
    print("No duplicates found.")

# ==========================================
# 3. FIX DATA TYPES
# ==========================================
print("Standardizing data types...")

# Convert Timestamp
# Coerce errors will turn "24-24-2025" into NaT (Not a Time)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Convert Numeric Columns (handling strings like "Invalid_Time")
numeric_cols = ['session_duration', 'data_download_mb', 'transaction_amount', 'risk_score', 'login_hour', 'access_count', 'privilege_level', 'failed_logins', 'login_frequency']

for col in numeric_cols:
    if col in df.columns:
        # force to numeric, turn errors to NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')

# ==========================================
# 4. HANDLE MISSING VALUES
# ==========================================
print("Handling Missing Values...")

# Drop rows where critical timestamp is missing (from bad format)
nat_count = df['timestamp'].isna().sum()
if nat_count > 0:
    print(f"Dropping {nat_count} rows with invalid timestamps.")
    df.dropna(subset=['timestamp'], inplace=True)

# Impute Numeric Missing Values with Median
for col in numeric_cols:
    if col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            print(f"  - Imputed {missing} missing values in '{col}' with median: {median_val}")

# Impute Categorical Missing Values with Mode
categorical_cols = ['role', 'attack_type', 'user_id']
for col in categorical_cols:
    if col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            print(f"  - Imputed {missing} missing values in '{col}' with mode: {mode_val}")

# ==========================================
# 5. NORMALIZE CATEGORICAL VALUES
# ==========================================
print("Normalizing Categorical Values...")
# Fix "ADMIN", "admin ", "Empl" etc.
if 'role' in df.columns:
    # Title case: "Admin", "Employee"
    df['role'] = df['role'].astype(str).str.strip().str.title()
    # Fix specific abbreviation if needed
    df['role'] = df['role'].replace({'Empl': 'Employee', 'Admn': 'Admin'})
    print(f"  - Unique roles after cleaning: {df['role'].unique()}")

# ==========================================
# 6. VALIDATE VALUE RANGES & LOGIC
# ==========================================
print("Validating Value Ranges...")

# Ensure non-negative values
non_neg_cols = ['data_download_mb', 'transaction_amount', 'session_duration']
for col in non_neg_cols:
    if col in df.columns:
        neg_count = (df[col] < 0).sum()
        if neg_count > 0:
            print(f"  - Fixed {neg_count} negative values in '{col}' (converted to absolute).")
            df[col] = df[col].abs()

# Cap Extreme Outliers (Domain Knowledge based)
# We avoid IQR/Percentiles here because "Attacks" (Exfiltration/Fraud) are effectively "Outliers" 
# compared to normal traffic. We must NOT clean them away!
# We only want to remove the "Impossible" values injected as errors (e.g. 1 Billion).

# Defined Hard Limits based on System Specs
MAX_DOWNLOAD_MB = 50000    # Valid attacks are ~2000-10000. Errors are 1,000,000.
MAX_TRANSACTION_USD = 500000 # Valid abuse is ~60,000. Errors are 1,000,000,000.

if 'data_download_mb' in df.columns:
    outliers = (df['data_download_mb'] > MAX_DOWNLOAD_MB).sum()
    if outliers > 0:
        print(f"  - Capped {outliers} impossible values in 'data_download_mb' at {MAX_DOWNLOAD_MB}")
        df['data_download_mb'] = np.where(df['data_download_mb'] > MAX_DOWNLOAD_MB, MAX_DOWNLOAD_MB, df['data_download_mb'])

if 'transaction_amount' in df.columns:
    outliers = (df['transaction_amount'] > MAX_TRANSACTION_USD).sum()
    if outliers > 0:
        print(f"  - Capped {outliers} impossible values in 'transaction_amount' at {MAX_TRANSACTION_USD}")
        df['transaction_amount'] = np.where(df['transaction_amount'] > MAX_TRANSACTION_USD, MAX_TRANSACTION_USD, df['transaction_amount'])

# ==========================================
# 7. SAVE CLEANED DATASET
# ==========================================
final_rows = len(df)
print(f"Cleaning Complete. Rows: {initial_rows} -> {final_rows} (Dropped {initial_rows - final_rows})")
print(f"Saving to {output_path}...")
df.to_csv(output_path, index=False)
print("Done!")

# Preview
print("\nCleaned Data Stats:")
print(df[['transaction_amount', 'data_download_mb']].describe())
print("\nNull Value Check (Should be all 0):")
print(df.isnull().sum().sum())
