from flask import Flask

from homepage import homepage_bp
from homepage1 import homepage1_bp
from signup import signup_bp
from login import login_bp
from pages import pages_bp
from adminlogin import adminlogin_bp
from adminregister import adminregister_bp
from admin_bookings import admin_bookings_bp
from booking_details import booking_details_bp

app = Flask(__name__)
app.secret_key = "speedy_rentals_secret"

app.register_blueprint(homepage_bp)
app.register_blueprint(homepage1_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(adminlogin_bp)
app.register_blueprint(adminregister_bp)
app.register_blueprint(admin_bookings_bp)
app.register_blueprint(booking_details_bp)

if __name__ == "__main__":
    app.run(debug=True)
