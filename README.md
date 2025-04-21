# Fitness Club Information System

**Course Project** for **State University of Intelligent Technologies and Telecommunications**

**Student:** Koliukhov Oleksii

**Disciplines:**
- Організація баз даних та знань (Database and Knowledge Organization)
- Веб-технології та веб-дизайн (Web Technologies and Web Design)

---

## 📖 Project Description
This project implements an **Information System for Fitness Club Staff**, featuring:
- Role-based access: **Administrator**, **Registrar**, and **Trainer**
- Full **CRUD** functionality for entities: Clients, Subscriptions, Trainers, Rooms, Equipment, Trainings
- **Responsive web interface** built with Flask, HTML, CSS, and JavaScript
- **PostgreSQL** backend with SQLAlchemy ORM

Designed to streamline the management of clients, subscriptions, equipment, and schedules in a fitness club.

---

## 🚀 Features
- **Authentication & Authorization**: Secure login for three roles with different permissions
- **Administrator Dashboard**:
  - Manage Trainers, Rooms, Equipment (Create, Read, Update, Delete)
- **Registrar Dashboard**:
  - Manage Clients and Subscriptions
  - Schedule and view Trainings
- **Trainer Dashboard**:
  - View personal schedule of trainings
- **Dynamic Forms**:
  - Client creation with room & trainer selection
  - Subscription linked to specific client
  - Training scheduling with date/time picker
- **Real-time Filtering** and **Search** in tables
- **Modal Pop-ups** for create/edit forms

---

## 🛠️ Setup and Installation

### Prerequisites
- **Python 3.9+**
- **pip3**
- **PostgreSQL** (version 14 or higher)

### Clone Repository
```bash
git clone https://github.com/Kolyhov/OBDZ_Web.git
cd fitness-club-is
```

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Database Initialization
1. Start PostgreSQL service and ensure it runs on `localhost:5432`
2. Create database:
   ```sql
   CREATE DATABASE postgres;
   ```
3. Update `app.config['SQLALCHEMY_DATABASE_URI']` in `app.py` if needed.
4. Initialize tables and sample users:
   ```bash
   python3 create_users.py
   ```

### Running the Application
```bash
python3 app.py
```
Open your browser at `http://127.0.0.1:5000` and log in:
- **Administrator:** `admin / adminpass`
- **Registrar:** `reg / regpass`
- **Trainer:** `trener / trenerpass`

---

## 📂 Project Structure
```
├── app.py               # Main Flask application
├── create_users.py      # Script to initialize DB and users
├── templates/           # HTML templates
│   ├── login.html
│   ├── admin.html
│   ├── registrar.html
│   └── trener.html
├── static/              # CSS and JS assets
│   └── style.css
├── app.py               # SQLAlchemy model definitions
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── FitnessServer Backup # PgAdmin Server Backup
```

---

## 🔧 Usage
1. **Administrator**:
   - Manage trainers, rooms, equipment
2. **Registrar**:
   - Enroll clients, create subscriptions, schedule trainings
3. **Trainer**:
   - View personal training schedule

All operations are available via intuitive web forms and modal dialogs.

---

## 📚 Technologies Used
- **Flask** – micro web framework
- **SQLAlchemy** – ORM for Python
- **PostgreSQL** – relational database
- **HTML5 & CSS3** – markup and styling
- **JavaScript** – dynamic behaviors and form handling

---

## 🎓 Coursework Context
This project was developed independently as a term project for the courses:
- **Database and Knowledge Organization**
- **Web Technologies and Web Design**

at the **State University of Intelligent Technologies and Telecommunications**.

---

© 2025 Koliukhov Oleksii