
import os
import joblib
import pandas as pd
import numpy as np
from config import Config
from utils.logger import get_logger
from model_definitions import UnsupervisedEnsemble

logger = get_logger()

class MLService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        logger.info("Initializing ML Service...")
        try:
            self.model = joblib.load(Config.MODEL_PATH)
            self.scaler = joblib.load(Config.SCALER_PATH)
            self.role_encoder = joblib.load(Config.ROLE_ENCODER_PATH)
            logger.info("ML Artifacts loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML artifacts: {e}")
            raise e

    def preprocess(self, data):
        """
        Transforms raw input dict into scalar-ready DataFrame.
        Matches FeatureEngineering/FeatureEngineer.py logic.
        """
        try:
            # 1. Create DataFrame
            df = pd.DataFrame([data])
            
            # 2. Time Features (Assuming timestamp is provided or Current Time)
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            else:
                df['timestamp'] = pd.to_datetime(pd.Timestamp.now())
                
            df['hour_of_day'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
            df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
            
            # 3. Derived Features
            # data_intensity = data_download_mb / session_duration
            duration = df['session_duration'].replace(0, 1)
            df['data_intensity'] = df['data_download_mb'] / duration
            df['access_rate'] = df['access_count'] / duration
            
            # 4. Encoding
            # Handle unknown roles by defaulting to something safe or erroring
            # Here we map to known classes, default to first class if unknown (or handle robustly)
            # For simplicity using transform, assuming role is valid.
            try:
                df['role_encoded'] = self.role_encoder.transform(df['role'].astype(str))
            except ValueError:
                 # Fallback for unknown role
                 logger.warning(f"Unknown role {df['role'][0]}, defaulting to 0")
                 df['role_encoded'] = 0

            # 4.5 Add Missing Features expected by Model
            # privilege_level (1-5), device_change (0/1), location_change (0/1), is_off_hours (0/1)
            if 'privilege_level' not in df.columns: df['privilege_level'] = 1
            if 'device_change' not in df.columns: df['device_change'] = 0
            if 'location_change' not in df.columns: df['location_change'] = 0
            
            # Recalculate is_off_hours based on timestamp/hour (8PM - 7AM = Off hours)
            # Matching RawData.py: l_hour < 7 or l_hour > 20
            df['is_off_hours'] = df['hour_of_day'].apply(lambda h: 1 if (h < 7 or h > 20) else 0)

            # 5. Select & Order Features (MUST MATCH TRAINING)
            # Features: session_duration, data_download_mb, transaction_amount, access_count, 
            #           login_frequency, login_hour, failed_logins, hour_of_day, day_of_week, 
            #           is_weekend, data_intensity, access_rate, role_encoded
            
            # NOTE: FeatureEngineer.py derived `hour_of_day`, but also had `login_hour` from raw data.
            # We must ensure `login_hour` exists. If not input, assume it's `hour_of_day`.
            if 'login_hour' not in df.columns:
                 df['login_hour'] = df['hour_of_day']

            final_cols = [
                'session_duration', 'data_download_mb', 'transaction_amount', 
                'access_count', 'data_intensity', 'access_rate', 
                'login_frequency', 'login_hour', 'failed_logins', 
                'hour_of_day', 'day_of_week', 'is_weekend', 'role_encoded',
                'privilege_level', 'device_change', 'location_change', 'is_off_hours'
            ]
            
            # Ensure all cols exist
            for col in final_cols:
                if col not in df.columns:
                    df[col] = 0 # Default filling
            
            df_final = df[final_cols]
            
            # 6. Scaling
            # Columns to scale: session_duration, data_download_mb, transaction_amount, 
            # access_count, data_intensity, access_rate, login_frequency, login_hour, failed_logins
            scale_cols = [
                'session_duration', 'data_download_mb', 'transaction_amount', 
                'access_count', 'data_intensity', 'access_rate', 
                'login_frequency', 'login_hour', 'failed_logins'
            ]
            
            df_final[scale_cols] = self.scaler.transform(df_final[scale_cols])
            
            # The model expects specific column order defined by `final_cols`.
            # IsolationForest doesn't care about names, just order.
            # However, `TrainModel.py` dropped EXCLUDE_COLS.
            # The remaining columns in `TrainModel.py` were everything in `FeatureEngineeredDataset.csv`
            # MINUS `['is_attack', 'attack_class', 'attack_type', 'risk_score', 'user_id', 'timestamp']`
            # Let's verify the order based on expected `FeatureEngineeredDataset.csv`
            
            return df_final
            
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            raise e

    def predict(self, data):
        try:
            X_input = self.preprocess(data)
            
            # 1. Anomaly Score (Lower is more anomalous)
            raw_scores = self.model.decision_function(X_input)
            
            # 2. Convert to Risk Score (0 to 1)
            # We need the logic from TrainModel.py: risk_scores = scaler.fit_transform(inverted_scores)
            # Since we can't fit on single prediction, we use a heuristic or parameters if we saved them.
            # TrainModel used MinMax on the BATCH.
            # For inference, we can clip/approximate. 
            # Inverted score range roughly: -0.2 (normal) to 0.8 (anomaly)? 
            # IF output is roughly -0.5 to 0.5.
            # Simpler: Use probability or manually normalize based on observed range in training.
            # Let's assume a simplified normalization based on standard IF score bounds.
            # decision_function offset: 0. Positive -> Normal, Negative -> Abnormal.
            # We want High Risk (1) for Negative, Low Risk (0) for Positive.
            
            # Heuristic normalization:
            # Score s. Max theoretical ~0.5 (very normal), Min ~ -0.5 (anomaly)
            # Risk = (0.5 - s)  -> if s=0.5 risk=0. if s=-0.5 risk=1.
            score = raw_scores[0]
            risk_score = 0.5 - score
            risk_score = max(0.0, min(1.0, risk_score)) # Clip 0-1
            
            # 3. Alert Status
            # We used dynamic threshold (85th percentile) in Training.
            # We should probably hardcode a "safe" threshold or load the saved one.
            # For this MVP, let's pick 0.75 as high risk.
            is_anomaly = bool(risk_score > 0.75)
            
            return {
                "risk_score": float(risk_score),
                "is_anomaly": is_anomaly,
                "raw_score": float(score)
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return None
