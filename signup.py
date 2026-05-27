from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3
import re
from werkzeug.security import generate_password_hash

signup_bp = Blueprint("signup", __name__)

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        # Password validation
        pattern = r'^(?=.*[A-Z])(?=.*\d).{8,}$'
        if not re.match(pattern, password):
            flash("Password must be at least 8 characters, include 1 uppercase letter and 1 number")
            return redirect(url_for("signup.signup"))

        # Confirm password
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("signup.signup"))

        # Email validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            flash("Invalid email format")
            return redirect(url_for("signup.signup"))

        # Hash the password
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_password)
            )
            conn.commit()
            flash("Signup successful! Please login.")
            return redirect(url_for("login.login"))
        except sqlite3.IntegrityError:
            flash("Email already exists!")
        finally:
            conn.close()

    return render_template("signup.html")
