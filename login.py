from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__)

@login_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("homepage.homepage"))

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user["email"]
            return redirect(url_for("homepage1.homepage1"))
        else:
            flash("Invalid email or password")

    return render_template("login.html")

# ---------------- FORGOT PASSWORD ----------------
@login_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        new_password = request.form["new_password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if user:
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash(new_password)
            conn.execute(
                "UPDATE users SET password=? WHERE email=?",
                (hashed_password, email)
            )
            conn.commit()
            flash("Password updated successfully. Please login.")
            conn.close()
            return redirect(url_for("login.login"))
        else:
            flash("Email not found")
            conn.close()

    return render_template("forgot_password.html")
