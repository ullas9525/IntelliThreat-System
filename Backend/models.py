
from database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Analyst') # IT Admin, HR, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Raw Features (Logged from Client/System)
    session_duration = db.Column(db.Float, nullable=False)
    data_download_mb = db.Column(db.Float, nullable=False)
    transaction_amount = db.Column(db.Float, nullable=False)
    access_count = db.Column(db.Integer, nullable=False)
    login_frequency = db.Column(db.Integer, nullable=False)
    failed_logins = db.Column(db.Integer, nullable=False)
    
    # Context
    ip_address = db.Column(db.String(50))
    action_type = db.Column(db.String(100))
    
    # Relationship
    user = db.relationship('User', backref=db.backref('logs', lazy=True))
    prediction = db.relationship('Prediction', backref='log', uselist=False, lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else f"User #{self.user_id}",
            'role': self.user.role if self.user else "Employee",
            'timestamp': self.timestamp.isoformat(),
            'action_type': self.action_type,
            'ip_address': self.ip_address or 'N/A',
            'risk_score': self.prediction.risk_score if self.prediction else None,
            'is_anomaly': self.prediction.is_anomaly if self.prediction else None
        }

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('activity_logs.id'), nullable=False)
    
    risk_score = db.Column(db.Float, nullable=False)
    is_anomaly = db.Column(db.Boolean, nullable=False)
    anomaly_type = db.Column(db.String(100)) # e.g. "High Data Exfiltration" (Inferred)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
