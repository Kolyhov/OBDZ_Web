from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # можешь поменять

# 🔗 Подключение к PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======= МОДЕЛИ =======
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, trener, registrar

class Trener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trener_id = db.Column(db.Integer, db.ForeignKey('trener.id'), nullable=False)
    date_time = db.Column(db.String(50))


# ======= МАРШРУТЫ =======
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'registrar':
                return redirect(url_for('registrar_dashboard'))
            elif user.role == 'trener':
                return redirect(url_for('trener_dashboard'))
        return render_template('login.html', error='Неверный логин или пароль')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/registrar')
def registrar_dashboard():
    if session.get('role') != 'registrar':
        return redirect(url_for('login'))
    return render_template('registrar.html')

@app.route('/trener')
def trener_dashboard():
    if session.get('role') != 'trener':
        return redirect(url_for('login'))
    trener_id = session.get('user_id')
    trainings = Training.query.filter_by(trener_id=trener_id).all()
    return render_template('trener.html', trainings=trainings)

# ======= СТАРТ =======
if __name__ == '__main__':
    app.run(debug=True)
