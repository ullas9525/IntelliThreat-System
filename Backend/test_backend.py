
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000/api"

def print_step(msg):
    print(f"\n{'='*50}")
    print(f"STEP: {msg}")
    print(f"{'='*50}")

def test_backend():
    session = requests.Session()
    
    # 1. Register User
    print_step("Registering User")
    username = f"test_user_{int(time.time())}" # Unique user
    email = f"{username}@example.com"
    password = "securePassword123"
    
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "role": "Analyst"
    }
    
    try:
        res = session.post(f"{BASE_URL}/auth/register", json=payload)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.json()}")
        if res.status_code != 201:
            print("Registration Failed!")
            return
    except Exception as e:
        print(f"Connection Failed: {e}")
        print("Make sure the backend is running! (python app.py)")
        return

    # 2. Login
    print_step("Logging In")
    login_payload = {
        "username": username,
        "password": password
    }
    
    res = session.post(f"{BASE_URL}/auth/login", json=login_payload)
    print(f"Status: {res.status_code}")
    
    if res.status_code == 200:
        data = res.json()
        token = data.get('access_token')
        print(f"Login Successful! Token received.")
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print("Login Failed!")
        print(res.text)
        return

    # 3. Make Prediction (Low Risk Example)
    print_step("Testing Prediction (Normal Behavior)")
    # Data close to normal means
    normal_data = {
        "session_duration": 30.0,
        "data_download_mb": 10.0,
        "transaction_amount": 0,
        "access_count": 5,
        "login_frequency": 1,
        "failed_logins": 0,
        "role": "Analyst",
        "ip_address": "192.168.1.5",
        "action_type": "Routine Check"
    }
    
    res = session.post(f"{BASE_URL}/predict", json=normal_data, headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

    # 4. Make Prediction (High Risk Example)
    print_step("Testing Prediction (High Risk Behavior)")
    # Data representing anomaly (high download in short time)
    anomaly_data = {
        "session_duration": 5.0,
        "data_download_mb": 5000.0, # Huge download quick
        "transaction_amount": 100000,
        "access_count": 500,
        "login_frequency": 10,
        "failed_logins": 5,
        "role": "IT Admin", # Even admin shouldn't do this
        "ip_address": "10.0.0.99",
        "action_type": "Mass Export"
    }
    
    res = session.post(f"{BASE_URL}/predict", json=anomaly_data, headers=headers)
    print(f"Status: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")

    # 5. Get Logs
    print_step("Fetching Activity Logs")
    res = session.get(f"{BASE_URL}/logs", headers=headers)
    print(f"Status: {res.status_code}")
    logs = res.json()
    print(f"Retrieved logs raw: {logs}")
    if isinstance(logs, list) and len(logs) > 0:
        print("Latest Log:")
        print(json.dumps(logs[0], indent=2))
    else:
        print("No logs found or error response.")

if __name__ == "__main__":
    test_backend()
