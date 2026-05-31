from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = "skills_exchange_secret_key"

COURSES = [
    {
        "id": 1,
        "title": "Programming",
        "icon": "💻",
        "description": "Learn Python, JavaScript, and more from experienced developers.",
        "lessons": 24,
        "students": 142
    },
    {
        "id": 2,
        "title": "Web Design",
        "icon": "🎨",
        "description": "Master HTML, CSS, and modern design principles.",
        "lessons": 18,
        "students": 98
    },
    {
        "id": 3,
        "title": "Marketing",
        "icon": "📊",
        "description": "Grow your business with digital marketing strategies.",
        "lessons": 15,
        "students": 76
    },
    {
        "id": 4,
        "title": "Digital Painting",
        "icon": "🖌️",
        "description": "Create stunning digital art with professional techniques.",
        "lessons": 20,
        "students": 64
    }
]

def get_db():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="skills_exchange"
    )

# ---------- PUBLIC PAGES ----------

@app.route('/')
def home():
    return render_template('home.html', courses=COURSES)

@app.route('/courses')
def courses():
    return render_template('courses.html', courses=COURSES)

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = next((c for c in COURSES if c["id"] == course_id), None)
    if not course:
        return redirect(url_for('courses'))
    return render_template('course_detail.html', course=course)

@app.route('/about')
def about():
    return render_template('about.html')

# ---------- AUTH ----------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')

        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = user.get('is_admin', 0)
                flash('Welcome back!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Wrong username or password.', 'error')
        except Exception as e:
            flash('Database error. Please try again.', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not (username and email and password):
            flash('All fields are required.', 'error')
            return render_template('signup.html')

        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            existing = cursor.fetchone()

            if existing:
                cursor.close()
                conn.close()
                flash('Username or email already taken.', 'error')
                return render_template('signup.html')

            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed)
            )
            conn.commit()
            new_id = cursor.lastrowid
            cursor.close()
            conn.close()

            session['user_id'] = new_id
            session['username'] = username
            session['is_admin'] = 0
            flash('Account created! Welcome!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Database error. Please try again.', 'error')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ---------- PROFILE ----------

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

# ---------- ADMIN ----------

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
    except:
        users = []
    return render_template('admin.html', users=users, courses=COURSES)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('is_admin'):
        return redirect(url_for('home'))
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('User deleted.', 'success')
    except:
        flash('Error deleting user.', 'error')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.debug = True
    app.run()
