from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default='Analyst')
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    logs = relationship('ActivityLog', back_populates='user', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ActivityLog(Base):
    __tablename__ = 'activity_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Features
    session_duration = Column(Float, nullable=False)
    data_download_mb = Column(Float, nullable=False)
    transaction_amount = Column(Float, nullable=False)
    access_count = Column(Integer, nullable=False)
    login_frequency = Column(Integer, nullable=False)
    failed_logins = Column(Integer, nullable=False)

    # Context
    ip_address = Column(String(50))
    action_type = Column(String(100))

    # Relationships
    user = relationship('User', back_populates='logs')
    prediction = relationship('Prediction', back_populates='log', uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else f"User #{self.user_id}",
            'role': self.user.role if self.user else "Employee",
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'action_type': self.action_type,
            'ip_address': self.ip_address or 'N/A',
            'risk_score': self.prediction.risk_score if self.prediction else None,
            'is_anomaly': self.prediction.is_anomaly if self.prediction else None
        }

class Prediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, ForeignKey('activity_logs.id'), nullable=False)

    risk_score = Column(Float, nullable=False)
    is_anomaly = Column(Boolean, nullable=False)
    anomaly_type = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    log = relationship('ActivityLog', back_populates='prediction')
