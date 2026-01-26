
from app import create_app
from models import User, db
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt()

with app.app_context():
    username = "analyst_01"
    password = "securePassword123"
    
    existing = User.query.filter_by(username=username).first()
    if existing:
        print(f"User {username} already exists.")
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email="analyst@intellithreat.com", password_hash=hashed_password, role="Senior Analyst")
        db.session.add(user)
        db.session.commit()
        print(f"Successfully created user: {username}")
