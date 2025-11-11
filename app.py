from flask import Flask, render_template, request, redirect, flash, session, url_for
import sqlite3, os, datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # change this

DB_FILE = "messages.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
init_db()

# ---------- PUBLIC ROUTES ----------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    if not name or not email or not message:
        flash("Please fill all fields.", "error")
        return redirect('/')
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    flash("✅ Message sent successfully!")
    return redirect('/')

# ---------- ADMIN ROUTES ----------

ADMIN_USERNAME = "vijay"
ADMIN_PASSWORD = "81051"  # change this!

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "error")
            return redirect('/admin/login')
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin/login')
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        messages = conn.execute("SELECT * FROM messages ORDER BY created_at DESC").fetchall()
    return render_template('dashboard.html', messages=messages)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash("Logged out successfully.", "info")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
