from flask import Flask, render_template, redirect, url_for, flash, session, request
from functools import wraps
import os
import hashlib
import uuid     # <-- Add this import

app = Flask(__name__)


def get_db_connection():
    pass


def Generate_id():
    return str(uuid.uuid4())   # <-- Fully working UUID generator


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(password, hashed):
    return hashlib.sha256(password.encode()).hexdigest() == hashed


def login_Authentication(f):
    @wraps(f)
    def decorated_function(*args, **Kwargs):
        if 'User_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for("login"))
        return f(*args, **Kwargs)
    return decorated_function


def Role_Authentication(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **Kwargs):
            if 'role' not in session:
                flash('Access denied. Please log in.')
                return redirect(url_for("login"))
            if session['role'] not in allowed_roles:
                flash('Access denied. Insufficient privileges.')
                return redirect(url_for("home"))
            return f(*args, **Kwargs)
        return decorated_function
    return decorator


@app.route('/')
def home():
    if 'User_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for("login"))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        # TODO -> Database check here
    return render_template("login.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get('role', 'tenant')
        birth_date = request.form.get('date')
        gender = request.form.get("gender")

        existing_user = 0  # Replace with SQL query

        if existing_user:
            flash('Email already registered.')
            return render_template('register.html')

        user_id = Generate_id()
        hashed_pw = hash_password(password)

        # TODO -> SQL INSERT user here

        flash('Registration successful! Please log in.')
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route('/dashboard')
@login_Authentication
def dashboard():
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'technician':
        return redirect(url_for('technician_dashboard'))
    else:
        return redirect(url_for('tenant_dashboard'))


@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
    return render_template('admin_dashboard.html')


@app.route('/tech/dashboard')
def technician_dashboard():
    if session.get('role') != 'technician':
        flash('Access denied.')
        return redirect(url_for('dashboard'))
    return render_template('tech_dashboard.html')


@app.route('/tenant/dashboard')
def tenant_dashboard():
    if session.get('role') != 'tenant':
        flash('Access denied')
        return redirect(url_for('dashboard'))
    return render_template('tenant_dashboard.html')


@app.route('/logout')
def Logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
