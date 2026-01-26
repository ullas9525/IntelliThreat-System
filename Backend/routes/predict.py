
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
    # In a real app, maybe only Admin sees all logs, users see own.
    # For demo, returning all logs associated with the current user or 50 recent ones.
    logs = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).limit(50).all()
    return jsonify([log.to_dict() for log in logs]), 200
