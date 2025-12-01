from flask import Flask, render_template, redirect, url_for, flash, session, request
from functools import wraps

app = Flask(__name__)
app.secret_key = "demo-secret-key"

# --------------------- LOGIN PROTECTION -----------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'User_id' not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# --------------------- HOME -----------------------
@app.route('/')
def home():
    return render_template("home.html")

# --------------------- ABOUT -----------------------
@app.route('/about')
def about():
    return render_template("about.html")

# --------------------- REGISTER -----------------------
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        flash("Registration completed successfully!")
        return redirect(url_for("login"))
    return render_template("register.html")

# --------------------- LOGIN -----------------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role").lower()  # normalize to lowercase
        session['User_id'] = "demo-user"
        session['role'] = role
        flash("Logged in successfully!")
        return redirect(url_for("dashboard"))
    return render_template("login.html")

# --------------------- DASHBOARD ROUTER -----------------------
@app.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role').lower()
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'technician':
        return redirect(url_for('technician_dashboard'))
    else:
        return redirect(url_for('tenant_dashboard'))

# --------------------- FAKE DASHBOARD DATA -----------------------
fake_requests = [
    {"id": 1, "title": "Fix AC", "status": "Pending", "assigned_to_name": "Ali", "date": "2025-11-01"},
    {"id": 2, "title": "Paint Wall", "status": "Completed", "assigned_to_name": "Omar", "date": "2025-10-27"},
    {"id": 3, "title": "Plumbing Issue", "status": "Pending", "assigned_to_name": "Ahmed", "date": "2025-10-30"}
]

def get_dashboard_stats():
    total = len(fake_requests)
    completed = len([r for r in fake_requests if r['status'] == 'Completed'])
    pending = len([r for r in fake_requests if r['status'] == 'Pending'])
    return total, completed, pending

# --------------------- DASHBOARDS -----------------------
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if session.get('role').lower() != 'admin':
        flash("Access denied. Admin only.")
        return redirect(url_for('dashboard'))
    total, completed, pending = get_dashboard_stats()
    return render_template('admin_dashboard.html', total_requests=total,
                           completed_requests=completed, pending_requests=pending,
                           requests=fake_requests, role="Admin")

@app.route('/tech/dashboard')
@login_required
def technician_dashboard():
    if session.get('role').lower() != 'technician':
        flash("Access denied.")
        return redirect(url_for('dashboard'))
    total, completed, pending = get_dashboard_stats()
    return render_template('tech_dashboard.html', total_requests=total,
                           completed_requests=completed, pending_requests=pending,
                           requests=fake_requests, role="Technician")

@app.route('/tenant/dashboard')
@login_required
def tenant_dashboard():
    if session.get('role').lower() != 'tenant':
        flash("Access denied.")
        return redirect(url_for('dashboard'))
    total, completed, pending = get_dashboard_stats()
    return render_template('tenant_dashboard.html', total_requests=total,
                           completed_requests=completed, pending_requests=pending,
                           requests=fake_requests, role="Tenant")

# --------------------- PLACEHOLDER ROUTES -----------------------
@app.route('/add_request')
@login_required
def add_request():
    flash("Add request page placeholder.")
    return redirect(url_for('dashboard'))

@app.route('/view_requests')
@login_required
def view_requests():
    flash("View requests page placeholder.")
    return redirect(url_for('dashboard'))

@app.route('/delete_request')
@login_required
def delete_request():
    flash("Delete request page placeholder.")
    return redirect(url_for('dashboard'))

@app.route('/reports')
@login_required
def reports():
    flash("Reports page placeholder.")
    return redirect(url_for('dashboard'))

@app.route('/settings')
@login_required
def settings():
    flash("Settings page placeholder.")
    return redirect(url_for('dashboard'))

@app.route('/view_request/<int:request_id>')
@login_required
def view_request(request_id):
    req = next((r for r in fake_requests if r['id'] == request_id), None)
    if not req:
        flash("Request not found.")
        return redirect(url_for('dashboard'))
    return render_template("view_request.html", req=req)

# --------------------- LOGOUT -----------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("home"))

# --------------------- RUN APP -----------------------
if __name__ == "__main__":
    app.run(debug=True)
