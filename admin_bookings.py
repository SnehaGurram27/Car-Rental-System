from flask import Blueprint, render_template, session, jsonify, redirect, url_for
import sqlite3

admin_bookings_bp = Blueprint("admin_bookings", __name__)

# ----------------- DB HELPER -----------------
def get_db():
    conn = sqlite3.connect("bookings.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= ADMIN BOOKINGS PAGE =================
@admin_bookings_bp.route("/admin-bookings")
def bookings_page():
    if "admin_id" not in session:
        return redirect(url_for("adminlogin.adminlogin"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookings")
    bookings = cur.fetchall()
    conn.close()

    return render_template("admin_bookings.html", bookings=bookings)

# ================= CONFIRM BOOKING =================
@admin_bookings_bp.route("/confirm-booking/<int:booking_id>")
def confirm_booking(booking_id):
    conn = get_db()
    conn.execute("UPDATE bookings SET status='Confirmed' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()
    return jsonify({"new_status": "Confirmed"})

# ================= CANCEL BOOKING =================
@admin_bookings_bp.route("/cancel-booking/<int:booking_id>")
def cancel_booking(booking_id):
    conn = get_db()
    conn.execute("UPDATE bookings SET status='Cancelled' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()
    return jsonify({"new_status": "Cancelled"})

# ================= REMOVE BOOKING =================
@admin_bookings_bp.route("/remove-booking/<int:booking_id>")
def remove_booking(booking_id):
    try:
        conn = get_db()
        conn.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except:
        return jsonify({"success": False})

# ================= ADMIN LOGOUT =================
@admin_bookings_bp.route("/admin-logout", methods=["POST"])
def admin_logout():
    session.pop("admin_id", None)  # remove admin session
    return redirect(url_for("homepage.homepage"))  # redirect to homepage