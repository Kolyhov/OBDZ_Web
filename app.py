from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ===== MODELS =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, trener, registrar

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipments = db.relationship('Equipment', backref='room', lazy=True)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

class Trener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    spec = db.Column(db.String(100), nullable=False)
    main_room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    main_room = db.relationship('Room', backref='trainers', lazy=True)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    workout = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    reg_date = db.Column(db.Date, nullable=False)
    main_room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    trener_id = db.Column(db.Integer, db.ForeignKey('trener.id'), nullable=True)
    sub_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=True)

class Training(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    sub_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    trener_id = db.Column(db.Integer, db.ForeignKey('trener.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

# ===== AUTH & DASHBOARDS =====
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            session['user_id'], session['role'] = user.id, user.role
            return redirect(url_for(f"{user.role}_dashboard"))
        flash('Неверный логин или пароль')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
def admin_dashboard():
    if session.get('role')!='admin': return redirect(url_for('login'))
    trainers = Trener.query.all()
    rooms = Room.query.all()
    equipment = Equipment.query.all()
    return render_template('admin.html', trainers=trainers, rooms=rooms, equipment=equipment)

@app.route('/registrar')
def registrar_dashboard():
    if session.get('role')!='registrar': return redirect(url_for('login'))
    clients = Client.query.all()
    subs = Subscription.query.all()
    trainings = Training.query.all()
    trainers = Trener.query.all()
    rooms = Room.query.all()
    current_date = date.today()
    return render_template('registrar.html', clients=clients, subs=subs, trainings=trainings, trainers=trainers, rooms=rooms, current_date=current_date)

@app.route('/trener')
def trener_dashboard():
    if session.get('role')!='trener': return redirect(url_for('login'))
    trainings = Training.query.filter_by(trener_id=session['user_id']).all()
    return render_template('trener.html', trainings=trainings)

# ===== CRUD FOR ADMIN =====
@app.route('/admin/room/create', methods=['POST'])
def admin_create_room():
    db.session.add(Room(address=request.form['address'], capacity=request.form['capacity']))
    db.session.commit(); return redirect(url_for('admin_dashboard'))

@app.route('/admin/trener/create', methods=['POST'])
def admin_create_trener():
    db.session.add(Trener(
        name=request.form['name'], phone=request.form['phone'],
        spec=request.form['spec'], main_room_id=request.form['main_room_id']))
    db.session.commit(); return redirect(url_for('admin_dashboard'))

@app.route('/admin/room/edit/<int:id>', methods=['POST'])
def admin_edit_room(id):
    r = Room.query.get_or_404(id)
    r.address = request.form['address']
    r.capacity = request.form['capacity']
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/trener/edit/<int:id>', methods=['POST'])
def admin_edit_trener(id):
    t = Trener.query.get_or_404(id)
    t.name = request.form['name']
    t.phone = request.form['phone']
    t.spec = request.form['spec']
    t.main_room_id = request.form['main_room_id']
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/equipment/create', methods=['POST'])
def admin_create_equipment():
    db.session.add(Equipment(
        name=request.form['name'],
        state=request.form['state'],
        room_id=request.form['room_id'] or None
    ))
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/equipment/edit/<int:id>', methods=['POST'])
def admin_edit_equipment(id):
    e = Equipment.query.get_or_404(id)
    e.name = request.form['name']
    e.state = request.form['state']
    e.room_id = request.form['room_id'] or None
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/equipment/delete/<int:id>')
def admin_delete_equipment(id):
    e = Equipment.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/room/delete/<int:id>')
def admin_delete_room(id):
    # Оборудование из этого зала становится без зала
    Equipment.query.filter_by(room_id=id).update({'room_id': None})
    # Удаляем все тренировки, связанные с этим залом
    Training.query.filter_by(room_id=id).delete()
    r = Room.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/trener/delete/<int:id>')
def admin_delete_trener(id):
    t = Trener.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# ===== CRUD FOR REGISTRAR =====
@app.route('/registrar/client/create', methods=['POST'])
def reg_create_client():
    new_client = Client(
        name=request.form['name'],
        phone=request.form['phone'],
        reg_date=request.form['reg_date'],
        main_room_id=request.form['main_room_id'],
        trener_id=request.form['trener_id'] or None
    )
    db.session.add(new_client)
    db.session.commit()
    return redirect(url_for('registrar_dashboard'))

@app.route('/registrar/client/edit/<int:id>', methods=['POST'])
def reg_edit_client(id):
    c = Client.query.get_or_404(id)
    c.name = request.form['name']
    c.phone = request.form['phone']
    c.reg_date = request.form['reg_date']
    c.main_room_id = request.form['main_room_id']
    c.trener_id = request.form['trener_id'] or None
    db.session.commit()
    return redirect(url_for('registrar_dashboard'))

@app.route('/registrar/client/delete/<int:id>')
def reg_delete_client(id):
    c = Client.query.get_or_404(id)
    # Сначала обнуляем sub_id у клиента, чтобы не было ссылки на абонемент
    c.sub_id = None
    db.session.commit()
    # Удаляем все тренировки клиента
    Training.query.filter_by(client_id=c.id).delete()
    # Удаляем все абонементы клиента
    Subscription.query.filter_by(client_id=c.id).delete()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('registrar_dashboard'))

@app.route('/registrar/sub/create', methods=['POST'])
def reg_create_sub():
    new_sub = Subscription(
        start_date=request.form['start_date'],
        duration=int(request.form['duration']),
        workout=int(request.form['workout']),
        client_id=int(request.form['client_id'])
    )
    db.session.add(new_sub)
    db.session.commit()
    # Привязка абонемента к клиенту (делаем sub_id у клиента равным id нового абонемента)
    client = Client.query.get(new_sub.client_id)
    client.sub_id = new_sub.id
    db.session.commit()
    return redirect(url_for('registrar_dashboard'))

@app.route('/registrar/sub/edit/<int:sub_id>', methods=['POST'])
def reg_edit_sub(sub_id):
    sub = Subscription.query.get_or_404(sub_id)
    sub.start_date = request.form['start_date']
    sub.duration = int(request.form['duration'])
    sub.workout = int(request.form['workout'])
    db.session.commit()
    return redirect(url_for('registrar_dashboard'))

# ===== RUN =====
if __name__=='__main__':
    app.run(debug=True)
