
import pandas as pd
import os
from sklearn.model_selection import train_test_split

# ==========================================
# CONFIGURATION
# ==========================================
script_dir = os.path.dirname(os.path.abspath(__file__))
# Input: FeatureEngineeredDataset.csv in FeatureEngineering folder
input_path = os.path.join(script_dir, "..", "FeatureEngineering", "FeatureEngineeredDataset.csv")
train_output = os.path.join(script_dir, "train.csv")
test_output = os.path.join(script_dir, "test.csv")

# Resolve absolute paths
input_path = os.path.abspath(input_path)

print("--- Starting Unsupervised Data Splitting ---")

# ==========================================
# 1. LOAD DATA
# ==========================================
if not os.path.exists(input_path):
    print(f"Error: Input file not found at {input_path}")
    print("Please ensure Feature Engineering has been completed.")
    exit()

print(f"Loading data from {input_path}...")
df = pd.read_csv(input_path)
print(f"Total Rows: {len(df)}")

# ==========================================
# 2. SPLIT DATA (80/20)
# ==========================================
# UNSUPERVISED LEARNING PRINCIPLE:
# In anomaly detection, we often assume we do not have reliable labels for the majority of data.
# Using stratification on 'is_attack' or 'risk_score' would imply we know the labels beforehand,
# which introduces data leakage/bias in an unsupervised setting.
# Therefore, we use Pure Random Shuffling to simulate a realistic data stream.

print("Splitting data using Pure Random Shuffling (80% Train, 20% Test)...")
print("Note: Stratification is explicitly disabled to adhere to Unsupervised Learning constraints.")

train_df, test_df = train_test_split(
    df, 
    test_size=0.20, 
    random_state=42, 
    shuffle=True 
    # stratify=None (Default)
)

# ==========================================
# 3. SAVE OUTPUTS
# ==========================================
print(f"Saving Train Set ({len(train_df)} rows) to {train_output}...")
train_df.to_csv(train_output, index=False)

print(f"Saving Test Set ({len(test_df)} rows) to {test_output}...")
test_df.to_csv(test_output, index=False)

# Validation Stats
print("\n--- Split Statistics ---")
if 'is_attack' in df.columns:
    train_anomalies = train_df['is_attack'].sum()
    test_anomalies = test_df['is_attack'].sum()
    print(f"Train Anomalies (Natural Distribution): {train_anomalies} ({train_anomalies/len(train_df):.2%})")
    print(f"Test Anomalies (Natural Distribution):  {test_anomalies} ({test_anomalies/len(test_df):.2%})")

print("Done!")
