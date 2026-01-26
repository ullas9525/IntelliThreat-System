
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ml_service import MLService
from config import Config

print("Initializing MLService...")
service = MLService()

data = {
    'session_duration': 45.0,
    'data_download_mb': 15.0,
    'transaction_amount': 0,
    'access_count': 12,
    'login_frequency': 1,
    'failed_logins': 0,
    'role': 'Analyst',
    'action_type': 'Report Generation',
    'user_id': 1
}

print("Running predict...")
try:
    result = service.predict(data)
    print("Result:", result)
except Exception as e:
    print("CAUGHT EXCEPTION:")
    import traceback
    traceback.print_exc()
