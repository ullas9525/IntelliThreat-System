from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, ActivityLog, Prediction
from schemas import PredictRequest, PredictResponse, LogResponse
from utils.auth_utils import get_current_user
from services.ml_service import MLService
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Machine Learning Telemetry & Predictions"])
ml_service = MLService()

@router.post("/predict", response_model=PredictResponse)
def predict_telemetry(
    payload: PredictRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        data_dict = payload.model_dump()
        result = ml_service.predict(data_dict)

        if not result:
            raise HTTPException(status_code=500, detail="Prediction failed")

        # Save activity log
        log_entry = ActivityLog(
            user_id=current_user.id,
            timestamp=datetime.utcnow(),
            session_duration=payload.session_duration,
            data_download_mb=payload.data_download_mb,
            transaction_amount=payload.transaction_amount,
            access_count=payload.access_count,
            login_frequency=payload.login_frequency,
            failed_logins=payload.failed_logins,
            ip_address=payload.ip_address or "127.0.0.1",
            action_type=payload.action_type or "System Access"
        )
        db.add(log_entry)
        db.flush()

        # Save prediction anomaly result
        prediction_entry = Prediction(
            log_id=log_entry.id,
            risk_score=result['risk_score'],
            is_anomaly=result['is_anomaly'],
            anomaly_type="Insider Threat Alert" if result['is_anomaly'] else "Normal Activity",
            timestamp=datetime.utcnow()
        )
        db.add(prediction_entry)
        db.commit()

        return PredictResponse(
            risk_score=result['risk_score'],
            is_anomaly=result['is_anomaly'],
            raw_score=result['raw_score']
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs", response_model=List[LogResponse])
def get_logs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role in ['IT Admin', 'Admin', 'Senior Analyst', 'Analyst']:
        logs = db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(100).all()
    else:
        logs = db.query(ActivityLog).filter(ActivityLog.user_id == current_user.id).order_by(ActivityLog.timestamp.desc()).limit(50).all()
        if not logs:
            logs = db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(50).all()
    return [l.to_dict() for l in logs]

@router.delete("/logs/{log_id}", response_model=dict)
def delete_log(log_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    log = db.query(ActivityLog).filter(ActivityLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")

    if log.prediction:
        db.delete(log.prediction)

    db.delete(log)
    db.commit()
    return {"msg": f"Log #{log_id} deleted successfully"}

@router.delete("/logs", response_model=dict)
def clear_all_logs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ['IT Admin', 'Admin']:
        raise HTTPException(status_code=403, detail="Admin privileges required to clear telemetry logs")

    try:
        db.query(Prediction).delete()
        db.query(ActivityLog).delete()
        db.commit()
        return {"msg": "All activity logs cleared successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to clear logs")
