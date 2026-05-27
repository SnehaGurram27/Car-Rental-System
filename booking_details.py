from flask import Blueprint, render_template, session, redirect, url_for, flash
import sqlite3

booking_details_bp = Blueprint("booking_details", __name__)

def get_db():
    conn = sqlite3.connect("bookings.db")
    conn.row_factory = sqlite3.Row
    return conn

@booking_details_bp.route("/booking-details")
def booking_details():
    # LOGIN REQUIRED
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("login.login"))

    user_id = session["user_id"]  # use user_id to fetch bookings

    # Fetch bookings for this user
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings WHERE user_id=? ORDER BY id DESC", (user_id,))
    bookings = cur.fetchall()
    conn.close()

    return render_template("booking_details.html", bookings=bookings)
