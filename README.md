EV Charging Ecosystem – Full-Stack Flask Application
A full-stack web application prototype that models an EV charging ecosystem in India, built to address real-world problems such as charger availability, booking management, user authentication, and admin control.
This project is designed as a scalable backend-first system, with clean separation of concerns, session-based authentication, and role-based access control.

🧠 Problem Statement
The EV charging ecosystem in India faces challenges beyond basic charging infrastructure:
Lack of real-time charger availability
No centralized booking management
Poor visibility for users
Limited admin control & analytics
This application demonstrates how these gaps can be addressed using a Flask-based full-stack architecture.

✨ Features

👤 User Features
User registration & login (session-based authentication)
Secure password hashing
View available EV chargers
Book charging slots
View booking history
Cancel bookings
Simulated payment flow

🧑‍💼 Admin Features
Role-based admin access
Add and manage EV chargers
View system statistics:
Total users
Total chargers
Total bookings
Revenue (simulated)
Admin dashboard

🛠️ Tech Stack
Backend
Python
Flask
Flask-SQLAlchemy
SQLite
Session-based authentication

Frontend
HTML5
CSS3
Bootstrap 5
Jinja2 Templates

Tooling
Git & GitHub
Virtual Environment (venv)
WSL (Linux-based development)

 Architecture Overview
Browser
   ↓
Flask Routes (Controllers)
   ↓
Business Logic
   ↓
SQLAlchemy ORM
   ↓
SQLite Database

Stateless HTTP + session-based memory
Database-driven state management
Role-based access control (RBAC)

🗂️ Project Structure
ev_charge_app/
│
├── app.py
├── config.py
├── requirements.txt
│
├── database/
│   └── ev_charge.db
│
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── user/
│   └── admin/
│
├── static/
│   ├── css/
│   └── js/
│
└── venv/

 Authentication & Security
Passwords are hashed using Werkzeug
Sessions store only user_id (no sensitive data)
Protected routes using session checks
Admin access enforced server-side

📊 Booking Lifecycle
ACTIVE → Slot reserved
CANCELLED → Slot released

Payment status:
PENDING
PAID (simulated)

This ensures:
No overbooking
Accurate slot tracking
Full booking history

🚀 How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/NikhilUpadhyay28/ev-charging-ecosystem.git
cd ev-charging-ecosystem

2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
python app.py


Open in browser:

http://127.0.0.1:5000

🧪 Notes on Database

SQLite is used for simplicity
During prototyping, the database was reset when schemas evolved
In production, migrations (Flask-Migrate/Alembic) would be used

📈 Future Enhancements
Google Maps / location-based charger search
Route planning
Payment gateway integration
REST API layer
Flask Blueprints for modularization
Deployment (Render / Railway)

🎯 What This Project Demonstrates
Full-stack development with Flask
Session-based authentication
Real-world booking logic
Role-based admin systems
Debugging real backend issues:
Redirect loops
Schema drift
Template context errors

👨‍💻 Author
Nikhil Upadhyay
Full-Stack Developer (Python, Flask)

GitHub:
👉 https://github.com/NikhilUpadhyay28
