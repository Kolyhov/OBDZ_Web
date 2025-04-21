from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    admin = User(username='admin', password_hash=generate_password_hash('adminpass', method='pbkdf2:sha256'), role='admin')
    reg = User(username='reg', password_hash=generate_password_hash('regpass', method='pbkdf2:sha256'), role='registrar')
    trener = User(username='trener', password_hash=generate_password_hash('trenerpass', method='pbkdf2:sha256'), role='trener')

    db.session.add_all([admin, reg, trener])
    db.session.commit()

    print("Пользователи успешно добавлены!")
