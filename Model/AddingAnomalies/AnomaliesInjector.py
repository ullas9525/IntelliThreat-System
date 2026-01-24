
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
df_original = pd.read_csv(input_path)
print(f"Original Shape: {df_original.shape}")

# We will separate the Original Data (Clean) and New Anomalies (Dirty)
# Policy: The original rows must remain untouched so we can compare later.
# We will create a set of "Bad Data" rows and APPEND them.

# Sample 15% of rows to create anomalies from
n_anomalies = int(len(df_original) * 0.15)
df_anomalies = df_original.sample(n=n_anomalies).copy()
print(f"Creating {n_anomalies} anomalous rows to append...")

# Reset index of anomalies for easier processing
df_anomalies = df_anomalies.reset_index(drop=True)
indices = df_anomalies.index.tolist()

# ==========================================
# 2. INTRODUCE MISSING VALUES (NaN)
# ==========================================
print("Injecting Missing Values (NaN)...")
missing_indices = random.sample(indices, int(n_anomalies * 0.30)) # 30% of anomalies

# Numeric Column Nulls
df_anomalies.loc[missing_indices[:len(missing_indices)//2], 'transaction_amount'] = np.nan
df_anomalies.loc[missing_indices[len(missing_indices)//2:], 'data_download_mb'] = np.nan

# Categorical Column Nulls
cat_missing_indices = random.sample(indices, int(n_anomalies * 0.20))
df_anomalies.loc[cat_missing_indices, 'role'] = np.nan

# ==========================================
# 3. INTRODUCE INVALID FORMATS (Dirty Strings)
# ==========================================
print("Injecting Invalid Formats (Strings in Numeric)...")
invalid_indices = random.sample(indices, int(n_anomalies * 0.10))

for idx in invalid_indices:
    if random.random() > 0.5:
        df_anomalies.at[idx, 'session_duration'] = "Invalid_Time"
    else:
        df_anomalies.at[idx, 'risk_score'] = "High_Risk"

# Malformed Timestamps
timestamp_indices = random.sample(indices, int(n_anomalies * 0.05))
for idx in timestamp_indices:
    df_anomalies.at[idx, 'timestamp'] = "24-24-2025" 

# ==========================================
# 4. INTRODUCE NEGATIVE VALUES (Logic Errors)
# ==========================================
print("Injecting Negative Values (Logical Errors)...")
negative_indices = random.sample(indices, int(n_anomalies * 0.10))

for idx in negative_indices:
    val = df_anomalies.at[idx, 'data_download_mb']
    if isinstance(val, (int, float)) and not pd.isna(val):
        df_anomalies.at[idx, 'data_download_mb'] = abs(val) * -1 

# ==========================================
# 5. INTRODUCE EXTREME OUTLIERS (Statistical Noise)
# ==========================================
print("Injecting Extreme Outliers...")
outlier_indices = random.sample(indices, int(n_anomalies * 0.10))

for idx in outlier_indices:
    df_anomalies.at[idx, 'transaction_amount'] = 999999999 
    df_anomalies.at[idx, 'data_download_mb'] = 1000000 

# ==========================================
# 6. INCONSISTENT CATEGORICAL VALUES
# ==========================================
print("Injecting Inconsistent Categories (Typos/Case)...")
typo_indices = random.sample(indices, int(n_anomalies * 0.30))

for idx in typo_indices:
    role_val = str(df_anomalies.at[idx, 'role'])
    if role_val.lower() == 'admin':
        choices = ['ADMIN', 'admin ', 'Admn'] 
        df_anomalies.at[idx, 'role'] = random.choice(choices)
    elif role_val.lower() == 'employee':
        df_anomalies.at[idx, 'role'] = 'empl'

# ==========================================
# 7. COMBINE AND SAVE
# ==========================================
# We append the anomalies to the original corrupted dataset
# In a real dirty dataset, you just get the dirty pile. 
# But to preserve the "Clean Truth" for comparison, we keep df_original intact acting as the "Pre-corruption" state.
# Wait, if we want AnomalyDataset to BE the dirty dataset, it should contain the dirty rows + clean rows.
# The user wants "CleanedDataset" == "RawDataset".
# RawDataset = [A, B, C]
# AnomalyDataset = [A, B, C, A', B'] (where A', B' are corrupt versions)
# CleanedDataset = Returns [A, B, C, A_fixed, B_fixed] (duplicates removed if exact).
# Actually, if we just want to ensure Raw and Cleaned rows match, we shouldn't touch A, B, C.

print("Merging Original and Anomalous Data...")
df_final = pd.concat([df_original, df_anomalies], ignore_index=True)

# Shuffle slightly so anomalies aren't just at the bottom (Realistic)
# df_final = df_final.sample(frac=1).reset_index(drop=True)
# COMMENTED OUT SHUFFLING to allow row-by-row comparison with RawDataset
# The original 100k rows will now be at the top, identical to RawDataset.

print(f"Final Shape: {df_final.shape}")
print(f"Saving to {output_path}...")
df_final.to_csv(output_path, index=False)
print("Done!")

# Preview
print("\nSample of Corrupted Data:")
print(df_final.tail(3))
