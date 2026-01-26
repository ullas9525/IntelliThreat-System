
import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, OutlierMixin

# ==========================================
# CONFIGURATION
# ==========================================
script_dir = os.path.dirname(os.path.abspath(__file__))
train_path = os.path.join(script_dir, "..", "SplitingData", "train.csv")
test_path = os.path.join(script_dir, "..", "SplitingData", "test.csv")
model_path = os.path.join(script_dir, "optimized_ensemble_model.pkl")
predictions_path = os.path.join(script_dir, "Predictions.csv")
plot_path = os.path.join(script_dir, "anomaly_score_distribution.png")

# Constraints (Unsupervised Principles)
EXCLUDE_COLS = ['is_attack', 'attack_class', 'attack_type', 'risk_score', 'user_id', 'timestamp']

from model_definitions import UnsupervisedEnsemble

# Optimization Config
# We use an ENSEMBLE of trees with different structures to capture different types of anomalies.
ENSEMBLE_GRID = [
    {'n_estimators': 100, 'max_samples': 256, 'max_features': 1.0},
    {'n_estimators': 200, 'max_samples': 256, 'max_features': 0.8}, # Subsample features
    {'n_estimators': 150, 'max_samples': 512, 'max_features': 1.0}, # Larger sample size
    {'n_estimators': 100, 'max_samples': 128, 'max_features': 1.0}, # Smaller sample size (sensitive to local anomalies)
]
CONTAMINATION_ESTIMATE = 0.15 
SELF_TRAINING_DROP_PCT = 0.05 # Drop top 5% "Noisiest" points from Train for Pass 2

def train_optimized_model():
    print("--- Starting Optimized Unsupervised Model Training ---")

    # 1. Load Data
    if not os.path.exists(train_path):
        print("Error: Train file missing.")
        exit()
    
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    print(f"Loaded Train: {train_df.shape}, Test: {test_df.shape}")

    # 2. Feature Selection (Strict Unsupervised)
    drop_cols_train = [c for c in EXCLUDE_COLS if c in train_df.columns]
    drop_cols_test = [c for c in EXCLUDE_COLS if c in test_df.columns]
    
    X_train = train_df.drop(columns=drop_cols_train)
    X_test = test_df.drop(columns=drop_cols_test)
    
    # 3. SELF-TRAINING (Pass 1)
    print("\n[Phase 1] Self-Training: Identifying Noise in Training Data...")
    ensemble_v1 = UnsupervisedEnsemble(ENSEMBLE_GRID, contamination=CONTAMINATION_ESTIMATE)
    ensemble_v1.fit(X_train)
    
    # Get scores on Training Data
    # Lower score = More Anomalous
    train_scores = ensemble_v1.decision_function(X_train)
    
    # Determine Cutoff to remove "obvious" anomalies from training
    # This helps the model define "Normal" more tightly in Pass 2.
    cutoff_threshold = np.percentile(train_scores, 100 * SELF_TRAINING_DROP_PCT) # e.g. 5th percentile
    
    mask_clean = train_scores > cutoff_threshold
    X_train_clean = X_train[mask_clean]
    print(f"  Filtered out {len(X_train) - len(X_train_clean)} noise points.")
    print(f"  Clean Training Set: {len(X_train_clean)} rows.")

    # 4. FINAL TRAINING (Pass 2)
    print("\n[Phase 2] Final Ensemble Training on Cleaned Data...")
    final_model = UnsupervisedEnsemble(ENSEMBLE_GRID, contamination=CONTAMINATION_ESTIMATE)
    final_model.fit(X_train_clean)
    
    # Save
    joblib.dump(final_model, model_path)
    print(f"Saved optimized model to {model_path}")

    # 5. PREDICTION & SCORING
    print("\nGenerating Predictions on Test Set...")
    raw_scores = final_model.decision_function(X_test)
    
    # Normalize Scores (0-1 Risk Score)
    # Reverse sign so High Score = High Risk
    inverted_scores = raw_scores * -1
    scaler = MinMaxScaler()
    risk_scores = scaler.fit_transform(inverted_scores.reshape(-1, 1)).flatten()
    
    # Adaptive Thresholding using Percentile
    # We expect roughly CONTAMINATION_ESTIMATE (15%) anomalies.
    # Set threshold at the 85th percentile of the risk distribution.
    adaptive_threshold = np.percentile(risk_scores, 100 * (1 - CONTAMINATION_ESTIMATE))
    print(f"Adaptive Risk Threshold (Top {CONTAMINATION_ESTIMATE:.0%}): {adaptive_threshold:.4f}")

    predictions = (risk_scores > adaptive_threshold).astype(int) # 1 = Alert

    # 6. RESULTS
    results = test_df.copy()
    results['predicted_risk'] = risk_scores
    results['is_alert'] = predictions
    results['threshold_used'] = adaptive_threshold
    
    results.to_csv(predictions_path, index=False)
    print(f"Saved predictions to {predictions_path}")

    # 7. EVALUATION (Hidden Labels)
    print("\n--- Model Evaluation (Using Hidden Ground Truth) ---")
    if 'is_attack' in results.columns:
        y_true = results['is_attack']
        y_pred = results['is_alert']
        
        tp = ((y_true == 1) & (y_pred == 1)).sum()
        fp = ((y_true == 0) & (y_pred == 1)).sum()
        fn = ((y_true == 1) & (y_pred == 0)).sum()
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"Alert Rate: {y_pred.mean():.2%}")

    # 8. PLOT
    plt.figure(figsize=(10, 6))
    plt.hist(risk_scores, bins=50, color='mediumpurple', alpha=0.7, label='Risk Scores')
    plt.axvline(adaptive_threshold, color='red', linestyle='--', label=f'Threshold ({adaptive_threshold:.2f})')
    plt.title("Distribution of Ensemble Risk Scores (Self-Trained)")
    plt.xlabel("Risk Probability")
    plt.ylabel("Frequency")
    plt.legend()
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    train_optimized_model()
