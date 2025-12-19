from flask import Flask, render_template, redirect, url_for, flash, session, request
from functools import wraps
import sqlite3
import hashlib
import uuid
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret-key-demo"

DB_NAME = "database.db"

# ----------------- DATABASE CONNECTION -----------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------- SETUP DATABASE ON FIRST RUN (FIXED) -----------------
def init_db():
    # --- FIX 1: Delete existing DB to ensure clean data/schema on startup ---
    if os.path.exists(DB_NAME):
        return
        #os.remove(DB_NAME)

    # Only proceed with creation if the file doesn't exist (which it won't after the line above)
    # The 'if not os.path.exists(DB_NAME):' is no longer strictly necessary but kept for flow
    # Since we removed the file, we proceed to create a new one:
    conn = get_db_connection()
    c = conn.cursor()

    # Create users table
    c.execute("""
    CREATE TABLE users (
        id TEXT PRIMARY KEY,
        fname TEXT,
        lname TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT,
        birth_date TEXT,
        gender TEXT
    )
    """)

    # Create requests table
    c.execute("""
    CREATE TABLE requests (
        id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        status TEXT,
        assigned_to TEXT,
        date TEXT,
        user_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(assigned_to) REFERENCES users(id)
    )
    """)

    # Insert test users
    test_users = [
        ("1", "Admin", "User", "admin@test.com",
         hashlib.sha256("123456".encode()).hexdigest(), "admin", "1990-01-01", "Male"),
        ("2", "Tenant", "User", "tenant@test.com",
         hashlib.sha256("123456".encode()).hexdigest(), "tenant", "1985-05-10", "Female"),
        ("3", "Tech", "User", "tech@test.com",
         hashlib.sha256("123456".encode()).hexdigest(), "technician", "1978-12-25", "Male"),
        ("4", "Another", "Tenant", "tenant2@test.com",
         hashlib.sha256("123456".encode()).hexdigest(), "tenant", "2000-03-15", "Female"),
        ("5", "Another", "Tenant", "tenant3@test.com",
         hashlib.sha256("123456".encode()).hexdigest(), "tenant", "2000-03-15", "male")
    ]
    

    c.executemany("""
    INSERT INTO users (id, fname, lname, email, password, role, birth_date, gender)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, test_users)

    # Insert test requests (Added a 'description' column for a more complete table)
    # Use current date/time for request submission
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_requests = [
        ("r1", "Fix AC", "AC is blowing hot air.", "Pending", "3", current_time, "2"),
        ("r2", "Paint Wall", "Need a fresh coat of white paint in the living room.", "Completed", "3", "2025-10-27 10:00:00", "2"),
        ("r3", "Plumbing Issue", "Leaky faucet in the kitchen sink.", "In Progress", "3", "2025-10-30 11:30:00", "4"),
        ("r4", "Broken Door", "Front door lock is jammed.", "Pending", "3", "2025-11-03 14:00:00", "4"),
        ("r5", "Electrical Wiring", "Outlet in bedroom sparking.", "Completed", "3", "2025-11-04 09:00:00", "2")
    ]

    #users = [
    #{"id": 1, "fname": "Admin", "lname": "User", "email": "admin@test.com", "role": "admin"},
    #{"id": 2, "fname": "Tenant", "lname": "User", "email": "tenant@test.com", "role": "tenant"},
    #{"id": 3, "fname": "Tech", "lname": "User", "email": "tech@test.com", "role": "technician"},
    #{"id": 4, "fname": "Another", "lname": "Tenant", "email": "tenant2@test.com", "role": "tenant"},
   # ]

    #requests = []

    c.executemany("""
    INSERT INTO requests (id, title, description, status, assigned_to, date, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, test_requests)

    conn.commit()
    conn.close()
    print("Database created and test accounts/requests added.")

init_db()

# ----------------- HELPERS -----------------
def Generate_id():
    return str(uuid.uuid4())

def hash_password(password):
    if not password:
        return None
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hashlib.sha256(password.encode()).hexdigest() == hashed

# ----------------- AUTH DECORATORS -----------------
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
                # --- FIX 2: Redirect to 'dashboard' instead of 'home' for logged-in users ---
                return redirect(url_for("dashboard")) 
            return f(*args, **Kwargs)
        return decorated_function
    return decorator

# ----------------- ROUTES -----------------
@app.route('/')
def home():
    if 'User_id' in session:
        return redirect(url_for('dashboard'))
    return render_template("Home.html")

# ----------------- LOGIN -----------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()

        if not user:
            flash("Email not found.")
            return render_template("login.html")

        if not check_password(password, user["password"]):
            flash("Incorrect password.")
            return render_template("login.html")

        session['User_id'] = user["id"]
        session['role'] = user["role"]
        session['name'] = user['fname'] + ' ' + user['lname']
        flash("Logged in successfully!")
        return redirect(url_for("dashboard"))

    return render_template("login.html")

# ----------------- REGISTER -----------------
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

        if not password:
            flash("Password is required.")
            return render_template("register.html")

        conn = get_db_connection()
        existing = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()

        if existing:
            flash('Email already registered.')
            conn.close()
            return render_template('register.html')

        user_id = Generate_id()
        hashed_pw = hash_password(password)

        conn.execute("""
        INSERT INTO users (id, fname, lname, email, password, role, birth_date, gender)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, fname, lname, email, hashed_pw, role, birth_date, gender))

        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.')
        return redirect(url_for("login"))

    return render_template("register.html")

# ----------------- DASHBOARD REDIRECT -----------------
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

# ----------------- ADMIN DASHBOARD -----------------
@app.route('/admin/dashboard', methods=['GET', 'POST'])
@Role_Authentication(["admin"])
def admin_dashboard():
    conn = get_db_connection()
    search_term = request.args.get('search', '')

    # Fetch tenants and technicians for create request form
    tenants = conn.execute("SELECT id, fname, lname FROM users WHERE role='tenant'").fetchall()
    technicians = conn.execute("SELECT id, fname, lname FROM users WHERE role='technician'").fetchall()

    # Handle Create Request form submission
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tenant_id = request.form.get('tenant')
        technician_id = request.form.get('technician')
        status = request.form.get('status', 'Pending')

        if not title or not description or not tenant_id:
            flash("Title, Description, and Tenant selection are required.", "error")
        else:
            req_id = Generate_id()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                "INSERT INTO requests (id, title, description, status, assigned_to, date, user_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (req_id, title, description, status, technician_id if technician_id != 'none' else None, date, tenant_id)
            )
            conn.commit()
            flash("Request created successfully!", "success")
            return redirect(url_for('admin_dashboard'))

    # Fetch recent requests (with search)
    query = """
        SELECT r.id, r.title, r.status, r.date, 
               u.fname AS assigned_fname, u.lname AS assigned_lname
        FROM requests r
        LEFT JOIN users u ON r.assigned_to = u.id
    """
    params = []
    if search_term:
        query += " WHERE r.title LIKE ? OR r.status LIKE ? "
        search_like = f'%{search_term}%'
        params.extend([search_like, search_like])
    query += " ORDER BY r.date DESC LIMIT 5"
    recent = conn.execute(query, params).fetchall()

    # Stats
    total_requests = conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    completed = conn.execute("SELECT COUNT(*) FROM requests WHERE status='Completed'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM requests WHERE status='Pending'").fetchone()[0]

    # Format recent requests
    formatted_recent = []
    for req in recent:
        assigned_to_name = f"{req['assigned_fname']} {req['assigned_lname']}" if req['assigned_fname'] else 'Unassigned'
        formatted_recent.append({
            'id': req['id'],
            'title': req['title'],
            'status': req['status'],
            'assigned_to': assigned_to_name,
            'date': req['date']
        })

    conn.close()

    return render_template('admin_dashboard.html', 
                           role=session.get('role'),
                           total_requests=total_requests, 
                           completed=completed,
                           pending=pending,
                           recent=formatted_recent,
                           tenants=tenants,
                           technicians=technicians,
                           search_term=search_term,
                           active_page='dashboard')


# ----------------- ADMIN - VIEW TENANT REQUESTS (NEW) -----------------
@app.route('/admin/tenant_view/<tenant_id>')
@Role_Authentication(["admin"])
def admin_view_tenant_requests(tenant_id):
    """Admin route to view a specific tenant's dashboard-style request summary."""
    conn = get_db_connection()
    
    # 1. Get the tenant's details
    tenant = conn.execute("SELECT id, fname, lname, email FROM users WHERE id = ? AND role = 'tenant'", (tenant_id,)).fetchone()
    
    if not tenant:
        flash("Tenant not found or user is not a tenant.", 'error')
        conn.close()
        return redirect(url_for('admin_users'))
    
    # 2. Get the tenant's requests and statistics
    total_requests = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE user_id = ?", (tenant_id,)
    ).fetchone()[0]
    
    completed = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE user_id = ? AND status='Completed'", (tenant_id,)
    ).fetchone()[0]
    
    in_progress = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE user_id = ? AND status IN ('Pending', 'In Progress')", (tenant_id,)
    ).fetchone()[0]
    
    # Recent requests (with assigned technician details)
    recent_requests_query = """
    SELECT r.id, r.title, r.status, r.date,
           u_tech.fname AS assigned_fname, u_tech.lname AS assigned_lname
    FROM requests r
    LEFT JOIN users u_tech ON r.assigned_to = u_tech.id
    WHERE r.user_id = ?
    ORDER BY r.date DESC
    LIMIT 10
"""
    recent_requests_data = conn.execute(recent_requests_query, (tenant_id,)).fetchall()

    conn.close()

    formatted_recent = []
    for req in recent_requests_data:
        assigned_to_name = f"{req['assigned_fname']} {req['assigned_lname']}" if req['assigned_fname'] else 'Unassigned'
        formatted_recent.append({
            'id': req['id'],
            'title': req['title'],
            'status': req['status'],
            'assigned_to': assigned_to_name,
            'date': req['date']
        })

    # You need a template named 'admin_tenant_view.html' for this
    return render_template('admin_tenant_view.html', 
                           tenant=tenant,
                           total_requests=total_requests, 
                           completed=completed,
                           in_progress=in_progress,
                           recent=formatted_recent,
                           role=session.get('role'),
                           active_page='users')

# ----------------- ADMIN - MANAGE SINGLE REQUEST (NEW) -----------------
@app.route('/admin/manage_request/<request_id>', methods=['GET', 'POST'])
@login_Authentication
@Role_Authentication(["admin"])
def admin_manage_request(request_id):
    """Admin route to view, update, assign, or delete a specific request."""
    conn = get_db_connection()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # --- Handle Status/Assignment Update ---
        if action == 'update_status' or action == 'assign_technician':
            new_status = request.form.get('status')
            new_assigned_to = request.form.get('assigned_to')

            if action == 'update_status' and new_status in ['Pending', 'In Progress', 'Completed']:
                conn.execute("UPDATE requests SET status = ? WHERE id = ?", (new_status, request_id))
                conn.commit()
                flash(f"Request {request_id} status updated to **{new_status}**.", 'success')
            
            elif action == 'assign_technician':
                # Set assigned_to to None (NULL) if 'none' is selected
                tech_id = new_assigned_to if new_assigned_to != 'none' else None
                conn.execute("UPDATE requests SET assigned_to = ? WHERE id = ?", (tech_id, request_id))
                conn.commit()
                flash(f"Request {request_id} assignment updated.", 'success')
        
        # --- Handle Deletion ---
        elif action == 'delete':
            conn.execute("DELETE FROM requests WHERE id = ?", (request_id,))
            conn.commit()
            conn.close()
            flash(f"Request {request_id} permanently deleted.", 'success')
            return redirect(url_for('admin_dashboard'))

        conn.close()
        return redirect(url_for('admin_manage_request', request_id=request_id))

    # --- Handle GET Request (Display) ---
    else:
        # Fetch the specific request details
        request_query = """
            SELECT r.*, 
                   u_tenant.fname AS tenant_fname, u_tenant.lname AS tenant_lname, u_tenant.email AS tenant_email,
                   u_tech.fname AS tech_fname, u_tech.lname AS tech_lname
            FROM requests r
            JOIN users u_tenant ON r.user_id = u_tenant.id
            LEFT JOIN users u_tech ON r.assigned_to = u_tech.id
            WHERE r.id = ?
        """
        request_data = conn.execute(request_query, (request_id,)).fetchone()
        
        if not request_data:
            conn.close()
            flash("Request not found.", 'error')
            return redirect(url_for('admin_dashboard'))

        # Fetch all technicians for the assignment dropdown
        technicians = conn.execute(
            "SELECT id, fname, lname FROM users WHERE role = 'technician'"
        ).fetchall()
        
        conn.close()

        assigned_name = f"{request_data['tech_fname']} {request_data['tech_lname']}" if request_data['tech_fname'] else 'Unassigned'
        
        # You need a template named 'admin_manage_request.html' for this
        return render_template('admin_manage_request.html', 
                               request_data=request_data, 
                               technicians=technicians,
                               assigned_name=assigned_name,
                               role=session.get('role'))


# ----------------- ADMIN - MANAGE USERS -----------------
@app.route('/admin/users')
@Role_Authentication(["admin"])
def admin_users():
    conn = get_db_connection()
    users = conn.execute(
        "SELECT id, fname, lname, email, role FROM users ORDER BY id"
    ).fetchall()
    conn.close()

    return render_template(
        'admin_users.html',
        users=users,
        active_page='users'
    )

# ----------------- ADMIN - ALL REQUESTS -----------------
@app.route('/admin/all_requests')
@Role_Authentication(["admin"])
def admin_all_requests():
    conn = get_db_connection()
    
    # Get all requests (with a JOIN to show the requesting user and assigned tech name)
    query = """
        SELECT r.id, r.title, r.description, r.status, r.date, 
               u_tech.fname AS assigned_fname, u_tech.lname AS assigned_lname,
               u_user.fname AS user_fname, u_user.lname AS user_lname
        FROM requests r
        LEFT JOIN users u_tech ON r.assigned_to = u_tech.id
        LEFT JOIN users u_user ON r.user_id = u_user.id
        ORDER BY r.date DESC
    """
    all_requests_data = conn.execute(query).fetchall()
    conn.close()
    
    # Format requests for the template
    formatted_requests = []
    for req in all_requests_data:
        assigned_to_name = f"{req['assigned_fname']} {req['assigned_lname']}" if req['assigned_fname'] else 'Unassigned'
        requested_by_name = f"{req['user_fname']} {req['user_lname']}" if req['user_fname'] else 'Unknown'
        formatted_requests.append({
            'id': req['id'],
            'title': req['title'],
            'status': req['status'],
            'assigned_to': assigned_to_name,
            'requested_by': requested_by_name,
            'date': req['date']
        })
    
    # A simple new template (admin_all_requests.html) would be best.
    return render_template('admin_all_requests.html', requests=formatted_requests, active_page='all_requests')

# ----------------- Admin Create Request -----------------
@app.route('/admin/create_request', methods=['GET', 'POST'])
@Role_Authentication(["admin"])
def admin_create_request():
    conn = get_db_connection()
    
    # Always load tenants/technicians for the form
    tenants = conn.execute("SELECT id, fname, lname FROM users WHERE role='tenant'").fetchall()
    technicians = conn.execute("SELECT id, fname, lname FROM users WHERE role='technician'").fetchall()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        user_id = request.form.get('user_id')        # ← matches your form name
        assigned_to = request.form.get('assigned_to') or None
        status = request.form.get('status', 'Pending')
        
        if not title or not description or not user_id:
            flash('Title, description, and tenant are required.', 'error')
        else:
            req_id = Generate_id()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute("""
                INSERT INTO requests (id, title, description, status, assigned_to, date, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (req_id, title, description, status, assigned_to, date, user_id))
            conn.commit()
            flash('Request created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
    
    conn.close()
    return render_template('admin_create_request.html', tenants=tenants, technicians=technicians)


# ================= TECHNICIAN ROUTES =================

@app.route('/tech/dashboard')
@login_Authentication
@Role_Authentication(['technician'])
def technician_dashboard():
    conn = get_db_connection()
    tech_id = session.get('User_id')

    # ---- Stats (same method as admin, but filtered) ----
    total = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE assigned_to = ?",
        (tech_id,)
    ).fetchone()[0]

    completed = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE assigned_to = ? AND status = 'Completed'",
        (tech_id,)
    ).fetchone()[0]

    pending = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE assigned_to = ? AND status = 'Pending'",
        (tech_id,)
    ).fetchone()[0]

    # ---- Table data (same idea as admin recent requests) ----
    jobs = conn.execute("""
        SELECT id, title, status, date
        FROM requests
        WHERE assigned_to = ?
        ORDER BY date DESC
    """, (tech_id,)).fetchall()

    conn.close()

    return render_template(
        'tech_dashboard.html',
        total=total,
        completed=completed,
        pending=pending,
        jobs=jobs,
        active_page='dashboard'
    )



@app.route('/tech/job-queue')
@login_Authentication
@Role_Authentication(['technician'])
def tech_job_queue():
    return render_template('tech-view-job-queue.html', active_page='job_queue')


@app.route('/tech/schedule')
@login_Authentication
@Role_Authentication(['technician'])
def tech_schedule():
    return render_template('tech_schedule.html', active_page='schedule')


@app.route('/tech/earnings')
@login_Authentication
@Role_Authentication(['technician'])
def tech_earnings():
    return render_template('tech_earnings.html', active_page='earnings')


@app.route('/tech/inventory')
@login_Authentication
@Role_Authentication(['technician'])
def tech_inventory():
    return render_template('tech_inventory.html', active_page='inventory')


@app.route('/tech/reports')
@login_Authentication
@Role_Authentication(['technician'])
def tech_reports():
    return render_template('tech_reports.html', active_page='reports')


@app.route('/tech/profile')
@login_Authentication
@Role_Authentication(['technician'])
def tech_profile():
    return render_template('tech_profile.html', active_page='profile')

@app.route('/tech/update_status/<request_id>', methods=['POST'])
@login_Authentication
@Role_Authentication(['technician'])
def tech_update_status(request_id):
    new_status = request.form.get('status')
    tech_id = session.get('User_id')

    if new_status not in ['In Progress', 'Completed']:
        flash("Invalid status.", "error")
        return redirect(url_for('technician_dashboard'))

    conn = get_db_connection()

    # Security check: technician can only update their own jobs
    job = conn.execute(
        "SELECT * FROM requests WHERE id = ? AND assigned_to = ?",
        (request_id, tech_id)
    ).fetchone()

    if not job:
        conn.close()
        flash("Unauthorized action.", "error")
        return redirect(url_for('technician_dashboard'))

    conn.execute(
        "UPDATE requests SET status = ? WHERE id = ?",
        (new_status, request_id)
    )
    conn.commit()
    conn.close()

    flash("Job status updated successfully.", "success")
    return redirect(url_for('technician_dashboard'))




# ----------------- TENANT DASHBOARD -----------------
@app.route('/tenant/dashboard')
@Role_Authentication(["tenant"])
def tenant_dashboard():
    tenant_id = session.get('User_id')
    search = request.args.get('search', '')

    conn = get_db_connection()

    # Stats
    total = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE user_id = ?", (tenant_id,)
    ).fetchone()[0]

    in_progress = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE user_id = ? AND status IN ('Pending', 'In Progress')", (tenant_id,)
    ).fetchone()[0]

    completed = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE user_id = ? AND status='Completed'", (tenant_id,)
    ).fetchone()[0]

    # Recent requests
    query = "SELECT id, title, status, date FROM requests WHERE user_id = ?"
    params = [tenant_id]
    if search:
        query += " AND title LIKE ?"
        params.append(f'%{search}%')
    query += " ORDER BY date DESC LIMIT 10"
    recent = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('tenant_dashboard.html', total=total, in_progress=in_progress,
                           completed=completed, recent=recent, search=search)

# ----------------- SUBMIT REQUEST -----------------
@app.route('/tenant/submit_request', methods=['GET', 'POST'])
@Role_Authentication(["tenant"])
def submit_request():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tenant_id = session.get('User_id')

        if not title or not description:
            flash("Title and Description are required.", "error")
            return render_template('tenant_submit_request.html')

        req_id = Generate_id()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO requests (id, title, description, status, assigned_to, date, user_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (req_id, title, description, "Pending", None, date, tenant_id)
        )
        conn.commit()
        conn.close()

        flash("Request submitted successfully!", "success")
        return redirect(url_for('tenant_dashboard'))

    return render_template('tenant_submit_request.html')

# ----------------- VIEW SINGLE REQUEST -----------------
@app.route('/tenant/request/<req_id>')
@Role_Authentication(["tenant"])
def view_single_request(req_id):
    tenant_id = session.get('User_id')
    conn = get_db_connection()
    req = conn.execute(
        "SELECT r.*, u.fname AS tenant_fname, u.lname AS tenant_lname "
        "FROM requests r JOIN users u ON r.user_id = u.id "
        "WHERE r.id = ? AND r.user_id = ?", (req_id, tenant_id)
    ).fetchone()
    conn.close()

    if not req:
        flash("Access Denied or Request not found.", 'error')
        return redirect(url_for('tenant_dashboard'))

    return render_template('tenant_view_request.html', request=req, role=session.get('role'))

@app.route('/admin/technician_view/<technician_id>')
@Role_Authentication(["admin"])
def admin_view_technician_requests(technician_id):
    conn = get_db_connection()

    tech = conn.execute(
        "SELECT id, fname, lname, email FROM users WHERE id = ? AND role = 'technician'",
        (technician_id,)
    ).fetchone()

    if not tech:
        flash("Technician not found.", "error")
        conn.close()
        return redirect(url_for('admin_users'))

    total_jobs = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE assigned_to = ?",
        (technician_id,)
    ).fetchone()[0]

    completed = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE assigned_to = ? AND status = 'Completed'",
        (technician_id,)
    ).fetchone()[0]

    in_progress = conn.execute(
        "SELECT COUNT(*) FROM requests WHERE assigned_to = ? AND status = 'In Progress'",
        (technician_id,)
    ).fetchone()[0]

    jobs = conn.execute("""
        SELECT id, title, status, date
        FROM requests
        WHERE assigned_to = ?
        ORDER BY date DESC
    """, (technician_id,)).fetchall()

    conn.close()

    return render_template(
        'admin_technician_view.html',
        technician=tech,
        total_jobs=total_jobs,
        completed=completed,
        in_progress=in_progress,
        jobs=jobs,
        active_page='users'
    )


# ----------------- ALL REQUESTS -----------------
@app.route('/tenant/requests')
@Role_Authentication(["tenant"])
def tenant_all_requests():
    tenant_id = session.get('User_id')
    conn = get_db_connection()
    all_requests = conn.execute(
        "SELECT id, title, status, date FROM requests WHERE user_id = ? ORDER BY date DESC", (tenant_id,)
    ).fetchall()
    conn.close()
    return render_template('tenant_all_requests.html', requests=all_requests, role=session.get('role'))


# ----------------- LOGOUT -----------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)