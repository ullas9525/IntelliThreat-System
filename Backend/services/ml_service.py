
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
            role_str = str(df['role'].iloc[0]).strip() if 'role' in df.columns else 'Employee'
            if hasattr(self.role_encoder, 'classes_') and role_str in self.role_encoder.classes_:
                df['role_encoded'] = self.role_encoder.transform([role_str])[0]
            else:
                role_map = {'Analyst': 'Employee', 'Senior Analyst': 'Employee', 'IT Admin': 'Admin', 'HR': 'Employee'}
                mapped_role = role_map.get(role_str, 'Employee')
                if hasattr(self.role_encoder, 'classes_') and mapped_role in self.role_encoder.classes_:
                    df['role_encoded'] = self.role_encoder.transform([mapped_role])[0]
                else:
                    df['role_encoded'] = 0

            # 4.5 Add Missing Features expected by Model
            if 'privilege_level' not in df.columns: df['privilege_level'] = 1
            if 'device_change' not in df.columns: df['device_change'] = 0
            if 'location_change' not in df.columns: df['location_change'] = 0
            
            # Recalculate is_off_hours based on timestamp/hour (8PM - 7AM = Off hours)
            df['is_off_hours'] = df['hour_of_day'].apply(lambda h: 1 if (h < 7 or h > 20) else 0)

            if 'login_hour' not in df.columns:
                df['login_hour'] = df['hour_of_day']

            # 5. Scaling
            scale_cols = getattr(self.scaler, 'feature_names_in_', [
                'session_duration', 'data_download_mb', 'transaction_amount', 
                'access_count', 'data_intensity', 'access_rate', 
                'login_frequency', 'login_hour', 'failed_logins'
            ])
            
            for col in scale_cols:
                if col not in df.columns:
                    df[col] = 0.0

            df[list(scale_cols)] = self.scaler.transform(df[list(scale_cols)])

            # 6. Select & Order Features (MUST MATCH MODEL TRAINING FIT ORDER EXACTLY)
            if hasattr(self.model, 'models') and len(self.model.models) > 0 and hasattr(self.model.models[0], 'feature_names_in_'):
                final_cols = list(self.model.models[0].feature_names_in_)
            else:
                final_cols = [
                    'login_hour', 'session_duration', 'data_download_mb', 'transaction_amount', 
                    'access_count', 'privilege_level', 'device_change', 'location_change', 
                    'failed_logins', 'is_off_hours', 'login_frequency', 'hour_of_day', 
                    'day_of_week', 'is_weekend', 'data_intensity', 'access_rate', 'role_encoded'
                ]
            
            for col in final_cols:
                if col not in df.columns:
                    df[col] = 0
            
            df_final = df[final_cols]
            return df_final
            
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            raise e

    def predict(self, data):
        try:
            X_input = self.preprocess(data)
            
            # 1. Anomaly Score (Lower is more anomalous)
            # 1. Anomaly Score (Lower/negative is anomalous in Isolation Forest)
            raw_scores = self.model.decision_function(X_input)
            score = raw_scores[0]
            
            # 2. Convert to Risk Score (0.0 to 1.0)
            # Isolation Forest decision_function ranges from ~ -0.35 (severe anomaly) to +0.25 (normal).
            # Score = 0.0 is the exact anomaly decision boundary (50% risk).
            risk_score = 0.5 - (score / 0.40)
            risk_score = max(0.0, min(1.0, risk_score)) # Clip to 0-1
            
            # 3. Alert Status
            # In Isolation Forest standard, any score < 0 (or risk_score > 0.50) is an anomaly
            is_anomaly = bool(score < 0 or risk_score > 0.50)
            
            return {
                "risk_score": float(risk_score),
                "is_anomaly": is_anomaly,
                "raw_score": float(score)
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return None

