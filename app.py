from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from config import Config



app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]


db = SQLAlchemy(app)
@app.context_processor
def inject_user():
    if "user_id" in session:
        return {"user": User.query.get(session["user_id"])}
    return {}

@app.context_processor
def inject_user():
    if "user_id" in session:
        return {"user": User.query.get(session["user_id"])}
    return {"user": None}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

class Charger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    charger_id = db.Column(db.Integer, db.ForeignKey("charger.id"), nullable=False)

    status = db.Column(db.String(20), default="ACTIVE")          # ACTIVE / CANCELLED
    payment_status = db.Column(db.String(20), default="PENDING") # PENDING / PAID
    amount = db.Column(db.Float, default=0.0)

    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

def get_current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None



@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("user/dashboard.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = get_current_user()
    if user.role != "admin":
        return redirect(url_for("dashboard"))

    total_users = User.query.count()
    total_chargers = Charger.query.count()
    total_bookings = Booking.query.count()

    total_revenue = db.session.query(
        db.func.sum(Booking.amount)
    ).filter(Booking.payment_status == "PAID").scalar() or 0

    return render_template(
        "admin/dashboard.html",
        user=user,
        total_users=total_users,
        total_chargers=total_chargers,
        total_bookings=total_bookings,
        total_revenue=total_revenue
    )

 
@app.route("/login", methods=["GET", "POST"])
def login():
    # 🔒 PROTECTION GOES HERE
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        flash("Logged in successfully!")
        return redirect(url_for("dashboard"))

    return render_template("auth/login.html")




@app.route("/signup", methods=["GET", "POST"])
def signup():
    # 🔒 PROTECTION GOES HERE
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)

        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(url_for("login"))

    return render_template("auth/signup.html")

@app.route("/admin/add-charger", methods=["GET", "POST"])
def add_charger():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        total_slots = int(request.form["total_slots"])

        charger = Charger(
            name=name,
            location=location,
            total_slots=total_slots,
            available_slots=total_slots
        )
        db.session.add(charger)
        db.session.commit()

        return "Charger Added"

    return render_template("admin/add_charger.html")

@app.route("/chargers")
def chargers():
    if "user_id" not in session:
        return redirect("/login")

    chargers = Charger.query.all()
    return render_template("user/chargers.html", chargers=chargers)


@app.route("/book/<int:charger_id>", methods=["POST"])
def book_charger(charger_id):
    if "user_id" not in session:
        flash("Login required")
        return redirect(url_for("login"))

    charger = Charger.query.get_or_404(charger_id)

    if not charger.is_active:
        flash("Charger inactive")
        return redirect(url_for("chargers"))

    if charger.available_slots <= 0:
        flash("No slots available")
        return redirect(url_for("chargers"))

    booking = Booking(
        user_id=session["user_id"],
        charger_id=charger.id
    )

    charger.available_slots -= 1

    db.session.add(booking)
    db.session.commit()

    flash("Booking successful ⚡")
    return redirect(url_for("chargers"))

@app.route("/cancel-booking/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    if "user_id" not in session:
        flash("Login required")
        return redirect(url_for("login"))

    booking = Booking.query.get_or_404(booking_id)

    # Security check
    if booking.user_id != session["user_id"]:
        flash("Unauthorized action")
        return redirect(url_for("my_bookings"))

    if booking.status == "CANCELLED":
        flash("Booking already cancelled")
        return redirect(url_for("my_bookings"))

    charger = Charger.query.get(booking.charger_id)

    booking.status = "CANCELLED"
    charger.available_slots += 1

    db.session.commit()

    flash("Booking cancelled, slot released")
    return redirect(url_for("my_bookings"))


@app.route("/my-bookings")
def my_bookings():
    if "user_id" not in session:
        return redirect("/login")

    bookings = db.session.query(Booking, Charger)\
        .join(Charger, Booking.charger_id == Charger.id)\
        .filter(Booking.user_id == session["user_id"])\
        .all()

    return render_template("user/my_bookings.html", bookings=bookings)

@app.route("/pay/<int:booking_id>", methods=["POST"])
def pay_booking(booking_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != session["user_id"]:
        flash("Unauthorized")
        return redirect(url_for("my_bookings"))

    booking.payment_status = "PAID"
    booking.amount = 200.0  # example flat rate

    db.session.commit()

    flash("Payment successful 💳")
    return redirect(url_for("my_bookings"))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully")
    return redirect(url_for("login"))


@app.route("/")
def home():
    return "EV Charging App Running"


if __name__ == "__main__":
    app.run(debug=True)
