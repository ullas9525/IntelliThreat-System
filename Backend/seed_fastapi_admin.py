from database import SessionLocal
from models import User
from utils.auth_utils import hash_password

db = SessionLocal()
try:
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@intellithreat.com",
            password_hash=hash_password("admin123"),
            role="IT Admin"
        )
        db.add(admin)
        db.commit()
        print("Created default admin user: admin / admin123")
    else:
        admin.password_hash = hash_password("admin123")
        admin.role = "IT Admin"
        db.commit()
        print("Verified admin user: admin / admin123")
finally:
    db.close()
