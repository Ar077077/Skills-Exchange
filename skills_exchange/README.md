# Skills Exchange

A community-driven learning platform where people teach each other.

## Courses
- 💻 Programming
- 🎨 Web Design
- 📊 Marketing
- 🖌️ Digital Painting

## Features
- User Registration & Login (with bcrypt password hashing)
- Course browsing & detail pages
- User profile page
- Admin panel (manage users)

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up the database
Open MySQL and run:
```bash
mysql -u root -p < schema.sql
```

### 3. Configure database connection
In `main.py`, update `get_db()` with your MySQL credentials:
```python
host="localhost"
port=3306
user="root"
password="your_password"
database="skills_exchange"
```

### 4. Run the app
```bash
python main.py
```

Visit: `http://localhost:5000`

## Admin Login
- Username: `admin`
- Password: `admin123`

> ⚠️ Change the admin password after first login!

## Project Structure
```
skills_exchange/
├── main.py              # Flask app
├── schema.sql           # Database setup
├── requirements.txt
├── Static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── home.html
    ├── courses.html
    ├── course_detail.html
    ├── login.html
    ├── signup.html
    ├── profile.html
    ├── about.html
    └── admin.html
```
