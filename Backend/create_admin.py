from app import create_app
from models import User, db
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt()

with app.app_context():
    admin_user = User.query.filter_by(username="admin").first()
    hashed_password = bcrypt.generate_password_hash("admin123").decode('utf-8')
    
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@intellithreat.com",
            password_hash=hashed_password,
            role="IT Admin"
        )
        db.session.add(admin_user)
        print("Created default admin user: admin")
    else:
        admin_user.password_hash = hashed_password
        admin_user.role = "IT Admin"
        print("Verified admin user: admin")

    db.session.commit()
    print("Admin provisioning complete.")
