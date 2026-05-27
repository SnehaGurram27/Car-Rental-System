from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash
import re

adminregister_bp = Blueprint("adminregister", __name__)

def get_db():
    return sqlite3.connect("admin.db")

@adminregister_bp.route("/admin-register", methods=["GET", "POST"])
def adminregister():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm-password"]

        # Password validation
        pattern = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
        if not re.match(pattern, password):
            flash("Password must be at least 8 characters, include 1 uppercase letter and 1 number", "danger")
            return redirect(url_for("adminregister.adminregister"))

        # Confirm password
        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for("adminregister.adminregister"))

        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            flash("Invalid email format", "danger")
            return redirect(url_for("adminregister.adminregister"))

        hashed = generate_password_hash(password)

        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO admin (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed)
            )
            conn.commit()
            conn.close()
            flash("Admin account created successfully", "success")
            return redirect(url_for("adminlogin.adminlogin"))

        except sqlite3.IntegrityError:
            flash("Email already exists", "danger")

    return render_template("adminregister.html")
