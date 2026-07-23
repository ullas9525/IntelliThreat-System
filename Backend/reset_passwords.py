from database import SessionLocal
from models import User
from utils.auth_utils import hash_password

db = SessionLocal()

try:
    print("Checking FastAPI database users...")
    users = db.query(User).all()
    for u in users:
        print(f"User ID: {u.id} | Username: {u.username} | Role: {u.role}")

    # Reset admin user
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        admin.password_hash = hash_password("admin123")
        admin.role = "IT Admin"
        print("Updated admin user password to: admin123")
    else:
        admin = User(
            username="admin",
            email="admin@intellithreat.com",
            password_hash=hash_password("admin123"),
            role="IT Admin"
        )
        db.add(admin)
        print("Created admin user: admin / admin123")

    # Reset analyst_01 user
    analyst = db.query(User).filter(User.username == "analyst_01").first()
    if analyst:
        analyst.password_hash = hash_password("securePassword123")
        print("Updated analyst_01 user password to: securePassword123")
    else:
        analyst = User(
            username="analyst_01",
            email="analyst@intellithreat.com",
            password_hash=hash_password("securePassword123"),
            role="Analyst"
        )
        db.add(analyst)
        print("Created analyst_01 user: analyst_01 / securePassword123")

    db.commit()
    print("FASTAPI DATABASE PASSWORDS SYNCED SUCCESSFULLY!")
finally:
    db.close()
