# 🎓 Besant Technologies – Student Portal

A fully functional **Flask + MySQL** web application for Besant Technologies, an IT training institute in Chennai. Students can register for free courses and mark attendance — no login or OTP required.

---

## 🌟 Features

| Feature | Description |
|--------|-------------|
| 🏠 Home Page | Hero banner, featured courses, testimonials, quick-action cards |
| 📚 Courses | 20+ courses grouped by category with live filters |
| 📝 Registration | Students fill a simple form to enrol — no account needed |
| ✅ Attendance | Students mark daily attendance by entering name + email |
| 📊 My Attendance | View full attendance history using email |
| 🛠️ Admin Panel | Dashboard with KPIs, registration list, attendance logs |
| 📬 Contact | Contact form stored in the database |

---

## 🛠️ Tech Stack

- **Backend**: Python 3 + Flask
- **Database**: MySQL (via Flask-MySQLdb)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Fonts / Icons**: Google Fonts (Inter, Poppins) + Font Awesome 6

---

## 📁 Project Structure

```
besant_tech/
├── app.py                   # Main Flask application
├── schema.sql               # MySQL database setup + seed data
├── requirements.txt         # Python dependencies
├── README.md
├── templates/
│   ├── base.html            # Base layout (navbar, footer, flash)
│   ├── index.html           # Home page
│   ├── courses.html         # All courses (filterable)
│   ├── register.html        # Course registration form
│   ├── register_success.html# Registration confirmation
│   ├── attendance.html      # Mark attendance form
│   ├── attendance_records.html # View attendance by email
│   ├── admin.html           # Admin dashboard
│   ├── admin_registrations.html
│   ├── admin_attendance.html
│   ├── about.html
│   └── contact.html
└── static/
    ├── css/
    │   └── style.css        # Full responsive stylesheet
    └── js/
        └── main.js          # Interactivity, filters, animations
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/besant-tech-portal.git
cd besant-tech-portal
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

On **Linux / macOS**, first install the MySQL dev headers:
```bash
sudo apt-get install libmysqlclient-dev   # Ubuntu/Debian
brew install mysql                         # macOS
```

Then install Python packages:
```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

Start MySQL and run the schema file:
```bash
mysql -u root -p < schema.sql
```

This creates the `besant_tech` database with all tables and seeds 20 courses automatically.

### 5. Configure Database Credentials

Open `app.py` and update:
```python
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = 'YOUR_MYSQL_PASSWORD'  # ← change this
app.config['MYSQL_DB']       = 'besant_tech'
```

### 6. Run the Application
```bash
python app.py
```

Visit **[(https://gangly-footing-unashamed.ngrok-free.dev )]** in your browser.

---

## 🗄️ Database Tables

| Table | Purpose |
|-------|---------|
| `courses` | All available courses |
| `registrations` | Student course enrolments |
| `attendance` | Daily attendance records |
| `contact_messages` | Contact form submissions |

---

## 🔗 Routes

| URL | Page |
|-----|------|
| `/` | Home |
| `/courses` | All Courses |
| `/register` | Registration Form |
| `/register/success/<id>` | Registration Confirmation |
| `/attendance` | Mark Attendance |
| `/attendance/records` | View My Attendance |
| `/admin` | Admin Dashboard |
| `/admin/registrations` | All Registrations |
| `/admin/attendance` | Attendance Logs |
| `/about` | About Page |
| `/contact` | Contact Page |

---

## 📸 Pages Overview

- **Home** — Hero, stats, features, featured courses, quick-action cards, testimonials
- **Courses** — Category filter, 20+ courses with duration and mode
- **Register** — Form with name, email, phone, gender, qualification, course
- **Attendance** — Name, email, course, date, session, status
- **Admin** — KPI cards, registration table, attendance by date, enrolment chart

---

## 🚀 Deploying to GitHub

```bash
git init
git add .
git commit -m "Initial commit – Besant Technologies Portal"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/besant-tech-portal.git
git push -u origin main
```

---

## 📄 License

MIT License – free to use and modify.

---

> Built with ❤️ for Besant Technologies, Chennai.
