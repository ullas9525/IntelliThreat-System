from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, ActivityLog
from schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from utils.auth_utils import hash_password, verify_password, create_jwt_token, get_current_user
from typing import List

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    if not user_data.username or not user_data.email or not user_data.password:
        raise HTTPException(status_code=400, detail="Missing required fields")

    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_pw,
        role=user_data.role or "Analyst"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = create_jwt_token(user.id)
    return {
        "access_token": access_token,
        "user": user.to_dict()
    }

@router.get("/users", response_model=List[UserResponse])
def get_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ['IT Admin', 'Admin']:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    users = db.query(User).order_by(User.created_at.desc()).all()
    return [u.to_dict() for u in users]

@router.delete("/users/{target_user_id}", response_model=dict)
def delete_user(target_user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ['IT Admin', 'Admin']:
        raise HTTPException(status_code=403, detail="Admin privileges required to delete users")

    if current_user.id == target_user_id:
        raise HTTPException(status_code=400, detail="Cannot delete your own admin account")

    target_user = db.query(User).filter(User.id == target_user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Cascade delete activity logs & predictions
    logs = db.query(ActivityLog).filter(ActivityLog.user_id == target_user_id).all()
    for log in logs:
        if log.prediction:
            db.delete(log.prediction)
        db.delete(log)

    db.delete(target_user)
    db.commit()
    return {"msg": f"User {target_user.username} deleted successfully"}
