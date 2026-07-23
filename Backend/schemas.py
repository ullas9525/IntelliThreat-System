from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "Analyst"

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    user: UserResponse

# ML Predict Payload Schema
class PredictRequest(BaseModel):
    session_duration: float
    data_download_mb: float
    transaction_amount: float
    access_count: int
    login_frequency: int
    failed_logins: int
    role: Optional[str] = "Analyst"
    action_type: Optional[str] = "System Access"
    ip_address: Optional[str] = "127.0.0.1"

class PredictResponse(BaseModel):
    risk_score: float
    is_anomaly: bool
    raw_score: float

# Activity Log Output Schema
class LogResponse(BaseModel):
    id: int
    user_id: int
    username: str
    role: str
    timestamp: str
    action_type: Optional[str] = None
    ip_address: Optional[str] = None
    risk_score: Optional[float] = None
    is_anomaly: Optional[bool] = None
