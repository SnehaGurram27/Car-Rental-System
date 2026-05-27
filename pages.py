from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

pages_bp = Blueprint("pages", __name__)

# ---------- DATABASE HELPER ----------
def get_db():
    conn = sqlite3.connect("bookings.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------- ADMIN LOGIN PAGE --------
@pages_bp.route("/admin-login")
def admin_login():
    return render_template("adminlogin.html")


# -------- ADMIN DASHBOARD (PROTECTED) --------
@pages_bp.route("/admin-dashboard")
def admin():
    if "admin_id" not in session:
        return redirect(url_for("adminlogin.adminlogin"))
    return render_template("admin.html")


# ================= STATIC PAGES =================
@pages_bp.route("/about")
def about():
    return render_template("about.html")


@pages_bp.route("/cars")
def cars():
    return render_template("car.html")


@pages_bp.route("/contact")
def contact():
    return render_template("contactus.html")


@pages_bp.route("/booking_details")
def booking_details():
    return render_template("booking_details.html")

# ---------------- BOOK CAR --------------------
@pages_bp.route("/bookcar", methods=["GET", "POST"])
def bookcar():

    # LOGIN REQUIRED
    if "user_id" not in session:
        flash("Please login first then book the car")
        return redirect(url_for("login.login"))

    # Autofill data from GET params
    pickup = request.args.get("pickup", "")
    drop = request.args.get("drop", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        car = request.form["car"]
        pickup = request.form["Pickup"]
        drop = request.form["drop"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        comments = request.form.get("comments", "")

        conn = get_db()
        conn.execute("""
            INSERT INTO bookings
            (user_id, name, email, phone, car, pickup, drop_location, start_date, end_date, comments, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
        """, (
            session["user_id"],
            name,
            email,
            phone,
            car,
            pickup,
            drop,
            start_date,
            end_date,
            comments
        ))
        conn.commit()
        conn.close()

        # SAVE EMAIL FOR BOOKING DETAILS PAGE
        session["user_email"] = email

        flash("Please wait for admin confirmation. Look Booking details page for updates")

    return render_template("bookcar.html", pickup=pickup, drop=drop, start_date=start_date, end_date=end_date)
