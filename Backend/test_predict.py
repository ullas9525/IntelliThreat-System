
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(script_dir, '..'))
model_dir = os.path.abspath(os.path.join(script_dir, '..', 'Model', 'ModelTraining'))

for p in [script_dir, root_dir, model_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

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
