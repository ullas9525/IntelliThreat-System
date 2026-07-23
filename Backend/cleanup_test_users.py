from app import create_app
from models import User, ActivityLog, Prediction, db

app = create_app()

with app.app_context():
    print("Purging test employee users...")
    test_users = User.query.filter(User.username.like('test_user_%')).all()
    
    count = 0
    for u in test_users:
        logs = ActivityLog.query.filter_by(user_id=u.id).all()
        for l in logs:
            if l.prediction:
                db.session.delete(l.prediction)
            db.session.delete(l)
        db.session.delete(u)
        count += 1

    db.session.commit()
    print(f"Purged {count} test user accounts from database!")

    remaining = User.query.all()
    print("Remaining Active Users:", [(u.id, u.username, u.role) for u in remaining])
