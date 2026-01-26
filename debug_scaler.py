
import joblib
import os
import pandas as pd

try:
    path = os.path.join("Model", "FeatureEngineering", "scaler.pkl")
    scaler = joblib.load(path)
    print(f"Scaler Features: {scaler.n_features_in_}")
    if hasattr(scaler, 'feature_names_in_'):
        print(f"Feature Names: {scaler.feature_names_in_}")
    else:
        print("Scaler does not have feature_names_in_ attribute.")
except Exception as e:
    print(f"Error: {e}")
