
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_change_in_prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:password@localhost/intellithreat_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_secret_key_change_in_prod'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # ML Model Config
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'ModelTraining', 'optimized_ensemble_model.pkl')
    SCALER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'FeatureEngineering', 'scaler.pkl')
    ROLE_ENCODER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'FeatureEngineering', 'role_encoder.pkl')
