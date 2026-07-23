
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import ActivityLog, Prediction, User, db
from services.ml_service import MLService
from utils.validators import validate_log_input
from utils.logger import get_logger

predict_bp = Blueprint('predict', __name__)
logger = get_logger()
ml_service = MLService()

@predict_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        data['user_id'] = user_id # Inject user_id for validation
        
        # Validate Input
        is_valid, msg = validate_log_input(data)
        if not is_valid:
            return jsonify({"msg": msg}), 400
            
        # 1. Run ML Inference
        # Enriched context needed for ML (e.g., role)
        # We might need to fetch the user role if not passed, but let's assume client sends 'role'
        # or we fetch it from DB if 'role' is missing in 'data'.
        if 'role' not in data:
            user = User.query.get(user_id)
            data['role'] = user.role if user else 'Analyst'
            
        result = ml_service.predict(data)
        
        if result:
            # 2. Save Log to DB
            new_log = ActivityLog(
                user_id=user_id,
                session_duration=data['session_duration'],
                data_download_mb=data['data_download_mb'],
                transaction_amount=data['transaction_amount'],
                access_count=data['access_count'],
                login_frequency=data['login_frequency'],
                failed_logins=data['failed_logins'],
                ip_address=data.get('ip_address', '127.0.0.1'),
                action_type=data.get('action_type', 'Unknown')
            )
            db.session.add(new_log)
            db.session.flush() # Get ID
            
            # 3. Save Prediction
            new_pred = Prediction(
                log_id=new_log.id,
                risk_score=result['risk_score'],
                is_anomaly=result['is_anomaly'],
                anomaly_type="High Risk Activity" if result['is_anomaly'] else "Normal"
            )
            db.session.add(new_pred)
            db.session.commit()
            
            logger.info(f"User {user_id} prediction: Risk={result['risk_score']:.2f}, Anomaly={result['is_anomaly']}")
            return jsonify(result), 200
        else:
            return jsonify({"msg": "Prediction failed"}), 500
            
    except Exception as e:
        logger.error(f"Predict route error: {e}")
        return jsonify({"msg": "Internal Server Error"}), 500

@predict_bp.route('/logs', methods=['GET'])
@jwt_required()
def get_logs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user and user.role in ['IT Admin', 'Admin', 'Senior Analyst', 'Analyst']:
        logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(100).all()
    else:
        logs = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).limit(50).all()
        if not logs:
            logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(50).all()
    return jsonify([log.to_dict() for log in logs]), 200

@predict_bp.route('/logs/<int:log_id>', methods=['DELETE'])
@jwt_required()
def delete_log(log_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    log = ActivityLog.query.get(log_id)
    
    if not log:
        return jsonify({"msg": "Log entry not found"}), 404
        
    # Delete associated prediction if exists
    if log.prediction:
        db.session.delete(log.prediction)
        
    db.session.delete(log)
    db.session.commit()
    logger.info(f"Log ID #{log_id} deleted by User #{user_id}")
    return jsonify({"msg": f"Log #{log_id} deleted successfully"}), 200

@predict_bp.route('/logs', methods=['DELETE'])
@jwt_required()
def clear_all_logs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role not in ['IT Admin', 'Admin']:
        return jsonify({"msg": "Admin privileges required to clear telemetry logs"}), 403
        
    try:
        Prediction.query.delete()
        ActivityLog.query.delete()
        db.session.commit()
        logger.info(f"All activity logs and predictions cleared by Admin #{user_id}")
        return jsonify({"msg": "All activity logs cleared successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to clear logs: {e}")
        return jsonify({"msg": "Failed to clear logs"}), 500
