from flask import Blueprint, request, jsonify
from models import User, db
from utils.validators import validate_register_input
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    is_valid, msg = validate_register_input(data)
    if not is_valid:
        return jsonify({"msg": msg}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400
        
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password, role=data.get('role', 'Analyst'))
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(access_token=access_token, user=user.to_dict()), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user or user.role not in ['IT Admin', 'Admin']:
        return jsonify({"msg": "Admin privileges required"}), 403
    
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users]), 200

@auth_bp.route('/users/<int:target_user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(target_user_id):
    current_user_id = int(get_jwt_identity())
    admin_user = User.query.get(current_user_id)
    
    if not admin_user or admin_user.role not in ['IT Admin', 'Admin']:
        return jsonify({"msg": "Admin privileges required to delete users"}), 403
        
    if current_user_id == target_user_id:
        return jsonify({"msg": "Cannot delete your own admin account"}), 400
        
    target_user = User.query.get(target_user_id)
    if not target_user:
        return jsonify({"msg": "User not found"}), 404
        
    from models import ActivityLog
    logs = ActivityLog.query.filter_by(user_id=target_user_id).all()
    for log in logs:
        if log.prediction:
            db.session.delete(log.prediction)
        db.session.delete(log)
        
    db.session.delete(target_user)
    db.session.commit()
    return jsonify({"msg": f"User {target_user.username} deleted successfully"}), 200
