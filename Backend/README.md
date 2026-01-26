
# IntelliThreat Backend

Flask-based backend for Unsupervised Insider Threat Detection.

## Setup

1.  **Navigate to backend**:
    ```bash
    cd backend
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Application**:
    ```bash
    python app.py
    ```
    The server will start at `http://localhost:5000`.

## API Endpoints

### 1. Register
**POST** `/api/auth/register`
```json
{
  "username": "analyst_01",
  "email": "analyst@company.com",
  "password": "securepassword123",
  "role": "Analyst"
}
```

### 2. Login
**POST** `/api/auth/login`
```json
{
  "username": "analyst_01",
  "password": "securepassword123"
}
```
**Response**:
```json
{
  "access_token": "eyJ0eXAi...",
  "user": { ... }
}
```

### 3. Predict & Log Activity
**POST** `/api/predict`
**Headers**: `Authorization: Bearer <access_token>`
```json
{
  "session_duration": 120.5,
  "data_download_mb": 5000.0,
  "transaction_amount": 0,
  "access_count": 50,
  "login_frequency": 1,
  "failed_logins": 0,
  "ip_address": "192.168.1.10",
  "action_type": "Large File Download"
}
```
**Response**:
```json
{
  "risk_score": 0.85,
  "is_anomaly": true,
  "raw_score": -0.15
}
```

### 4. Get History
**GET** `/api/logs`
**Headers**: `Authorization: Bearer <access_token>`
