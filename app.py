from flask import Flask, render_template, redirect, url_for, flash, session, request
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


def login_Authentication():
    pass


def Role_Authentication():
    pass


@app.route('//')
def home():
    return redirect(url_for('home'))


@app.route('//login')
def login():
    return render_template('login.html')


@app.route('//Register')
def register():
    return render_template('Register.html')


@app.route('//dashboard')
def dashboard():
    Role = session.get('Role','role')
    if Role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif Role == 'technician':
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


@app.route('//logout')
def Logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('home'))

    

if __name__ == '__main__':
    app.run(debug=True)
