from flask import Blueprint, render_template

homepage1_bp = Blueprint("homepage1", __name__)

@homepage1_bp.route("/homepage1")
def homepage1():
    return render_template("homepage1.html")

