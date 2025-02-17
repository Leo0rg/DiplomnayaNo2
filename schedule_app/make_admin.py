from app import app, db, User

with app.app_context():
    user = User.query.first()
    if user:
        user.is_admin = True
        db.session.commit()
        print(f'User {user.username} is admin')
    else:
        print('404') 