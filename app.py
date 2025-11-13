from flask import Flask, render_template, redirect, url_for, flash, session, request
from functools import wraps
import os

app = Flask(__name__)


def get_db_connection():
    pass


def Generate_id():
    pass


def hash_password():
    pass


def check_password():
    pass


def login_Authentication(f):
    @wraps(f)
    def decorated_function(*args, **Kwargs):
        if 'User_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for("login.html"))
        return f(*args , **Kwargs)
    return decorated_function



def Role_Authentication(allowed_roles):
    def decorator(f):
        @wraps
        def decorated_function(*args, **Kwargs):
            if 'role' not in session:
                flash('Access denied. Please log in.')
                return redirect(url_for("login.html"))
            if session ['role'] not in allowed_roles:
                flash('Access denied. Insufficient privileges.')
                return redirect(url_for("home.html"))
            return f(*args, **Kwargs)
        return decorated_function
    return decorator


@app.route('/')
def home():
    if 'User_id' in session:
        return redirect(url_for('home.html'))
    return redirect(url_for("login.html"))


@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # still dont know how to connect to database 
        #after connecting to the database we need sql to get email then there will be function to check the password 
        


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get('role','tenant') # why tenant? only to set it as default
        birth_date = request.form.get('date')
        gender = request.form.get("gender")

        #need the database connection to get SQL QUERY for all that.
        # at this line we should make database connection
        existing_user : 0 # that line were the SQL QUERY will be written 

        if existing_user:
            flash('Email already registered.')
            pass# i dont know what to return so i will pass i should return the database connection
            return render_template('Register.html')
        
        user_id = Generate_id()
        hashed_pw = hash_password()
        # database connection and insert the user id name nad email and role 

        flash('Registration successful! Please log in.')
        return redirect(url_for("login.html"))
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


@app.route('//admin/dashboard')
def admin_dashboard():
    if session.get('role','Role') != 'admin':
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('dashboard'))
    return render_template('admin_dashboard.html')


@app.route('//tech/dashboard')
def technician_dashboard():
    if session.get('role','Role') != 'technician':
        flash('Access denied.')
        return redirect(url_for('dashboard'))
    return render_template('tech_dashboard.html')


@app.route('//tenant/dashboard')
def tenant_dashboard():
    if session.get('role','Role') != 'tenant':
        flash('Access denied')
        return redirect(url_for('dashboard'))
    return render_template('tenant_dashboard.html')


@app.route('/logout')
def Logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('login.html'))

    

if __name__ == '__main__':
    app.run(debug=True)
