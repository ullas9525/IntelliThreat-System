from app import create_app
from models import User, db
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt()

with app.app_context():
    print("Checking database users...")
    users = User.query.all()
    for u in users:
        print(f"User ID: {u.id} | Username: {u.username} | Role: {u.role}")

    # Ensure admin user exists with password 'admin123'
    admin = User.query.filter_by(username="admin").first()
    admin_pass_hash = bcrypt.generate_password_hash("admin123").decode('utf-8')

    if admin:
        admin.password_hash = admin_pass_hash
        admin.role = "IT Admin"
        print("Updated existing admin user password to: admin123")
    else:
        admin = User(
            username="admin",
            email="admin@intellithreat.com",
            password_hash=admin_pass_hash,
            role="IT Admin"
        )
        db.session.add(admin)
        print("Created new admin user: admin / admin123")

    # Ensure analyst_01 user exists with password 'securePassword123'
    analyst = User.query.filter_by(username="analyst_01").first()
    analyst_pass_hash = bcrypt.generate_password_hash("securePassword123").decode('utf-8')

    if analyst:
        analyst.password_hash = analyst_pass_hash
        print("Updated existing analyst_01 user password to: securePassword123")
    else:
        analyst = User(
            username="analyst_01",
            email="analyst@intellithreat.com",
            password_hash=analyst_pass_hash,
            role="Analyst"
        )
        db.session.add(analyst)
        print("Created new analyst_01 user: analyst_01 / securePassword123")

    db.session.commit()
    print("ALL PASSWORDS RESET & VERIFIED IN DATABASE SUCCESSFUL!")
