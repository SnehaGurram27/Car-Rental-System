from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import re

adminlogin_bp = Blueprint("adminlogin", __name__)

def get_db():
    return sqlite3.connect("admin.db")

# CREATE TABLE IF NOT EXISTS
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

# ================= ADMIN LOGIN =================
@adminlogin_bp.route("/admin-login", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM admin WHERE email=?", (email,))
        admin = cur.fetchone()
        conn.close()

        if admin and check_password_hash(admin[1], password):
            session["admin_id"] = admin[0]
            return redirect(url_for("admin_bookings.bookings_page"))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("adminlogin.adminlogin"))

    return render_template("adminlogin.html")

# ================= FORGOT PASSWORD =================
@adminlogin_bp.route("/admin-forgot-password", methods=["GET", "POST"])
def admin_forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        new_password = request.form["new_password"]

        # Password validation
        pattern = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
        if not re.match(pattern, new_password):
            flash("Password must be at least 8 characters, include 1 uppercase letter and 1 number", "danger")
            return redirect(url_for("adminlogin.admin_forgot_password"))

        hashed_password = generate_password_hash(new_password)

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM admin WHERE email=?", (email,))
        admin = cur.fetchone()
        if admin:
            cur.execute("UPDATE admin SET password=? WHERE email=?", (hashed_password, email))
            conn.commit()
            flash("Password updated successfully", "success")
            conn.close()
            return redirect(url_for("adminlogin.adminlogin"))
        else:
            flash("Email not found", "danger")
            conn.close()

    return render_template("admin_forgot_password.html")
