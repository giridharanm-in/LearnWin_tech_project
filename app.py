from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from datetime import date, datetime
import os

app = Flask(__name__)
app.secret_key = 'besant_tech_secret_2024'

# ─── MySQL Configuration ───────────────────────────────────────────────────────
# Update these with your local MySQL credentials
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = ''          # ← put your MySQL root password here
app.config['MYSQL_DB']       = 'besant_tech'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# ───────────────────────────────────────────────────────────────────────────────
# ROUTES
# ───────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses ORDER BY created_at DESC")
    courses = cur.fetchall()
    cur.close()
    return render_template('index.html', courses=courses)


# ── Courses listing ─────────────────────────────────────────────────────────────
@app.route('/courses')
def courses():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses ORDER BY category, course_name")
    all_courses = cur.fetchall()
    cur.close()
    # Group by category
    grouped = {}
    for c in all_courses:
        cat = c['category']
        grouped.setdefault(cat, []).append(c)
    return render_template('courses.html', grouped=grouped)


# ── Course Registration ──────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses ORDER BY course_name")
    courses = cur.fetchall()

    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        email       = request.form.get('email', '').strip()
        phone       = request.form.get('phone', '').strip()
        course_id   = request.form.get('course_id', '').strip()
        gender      = request.form.get('gender', '').strip()
        qualification = request.form.get('qualification', '').strip()
        message     = request.form.get('message', '').strip()

        if not all([name, email, phone, course_id, gender, qualification]):
            flash('Please fill in all required fields.', 'error')
            cur.close()
            return render_template('register.html', courses=courses)

        # Check for duplicate registration
        cur.execute(
            "SELECT id FROM registrations WHERE email=%s AND course_id=%s",
            (email, course_id)
        )
        existing = cur.fetchone()
        if existing:
            flash('You have already registered for this course with this email.', 'warning')
            cur.close()
            return render_template('register.html', courses=courses)

        cur.execute(
            """INSERT INTO registrations
               (name, email, phone, course_id, gender, qualification, message, registered_on)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (name, email, phone, course_id, gender, qualification, message, date.today())
        )
        mysql.connection.commit()
        reg_id = cur.lastrowid
        cur.close()
        flash(f'Registration successful! Your Registration ID is #{reg_id}', 'success')
        return redirect(url_for('register_success', reg_id=reg_id))

    cur.close()
    return render_template('register.html', courses=courses)


@app.route('/register/success/<int:reg_id>')
def register_success(reg_id):
    cur = mysql.connection.cursor()
    cur.execute(
        """SELECT r.*, c.course_name, c.duration
           FROM registrations r
           JOIN courses c ON r.course_id = c.id
           WHERE r.id = %s""", (reg_id,)
    )
    reg = cur.fetchone()
    cur.close()
    return render_template('register_success.html', reg=reg)


# ── Attendance ───────────────────────────────────────────────────────────────────
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses ORDER BY course_name")
    courses = cur.fetchall()

    if request.method == 'POST':
        name      = request.form.get('name', '').strip()
        email     = request.form.get('email', '').strip()
        course_id = request.form.get('course_id', '').strip()
        att_date  = request.form.get('att_date', str(date.today())).strip()
        status    = request.form.get('status', 'Present').strip()
        session   = request.form.get('session', 'Morning').strip()

        if not all([name, email, course_id, att_date]):
            flash('Please fill all required fields.', 'error')
            cur.close()
            return render_template('attendance.html', courses=courses, today=date.today())

        # Check if attendance already marked
        cur.execute(
            """SELECT id FROM attendance
               WHERE email=%s AND course_id=%s AND att_date=%s AND session=%s""",
            (email, course_id, att_date, session)
        )
        already = cur.fetchone()
        if already:
            flash('Attendance already marked for this session today.', 'warning')
            cur.close()
            return render_template('attendance.html', courses=courses, today=date.today())

        cur.execute(
            """INSERT INTO attendance (name, email, course_id, att_date, status, session, marked_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (name, email, course_id, att_date, status, session, datetime.now())
        )
        mysql.connection.commit()
        cur.close()
        flash('Attendance marked successfully!', 'success')
        return redirect(url_for('attendance'))

    cur.close()
    return render_template('attendance.html', courses=courses, today=date.today())


# ── Attendance Records (view own) ────────────────────────────────────────────────
@app.route('/attendance/records', methods=['GET', 'POST'])
def attendance_records():
    records = []
    searched = False
    email_search = ''
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM courses ORDER BY course_name")
    courses = cur.fetchall()

    if request.method == 'POST':
        email_search = request.form.get('email', '').strip()
        searched = True
        if email_search:
            cur.execute(
                """SELECT a.*, c.course_name
                   FROM attendance a
                   JOIN courses c ON a.course_id = c.id
                   WHERE a.email = %s
                   ORDER BY a.att_date DESC""",
                (email_search,)
            )
            records = cur.fetchall()
    cur.close()
    return render_template('attendance_records.html',
                           records=records, searched=searched,
                           email_search=email_search, courses=courses)


# ── Admin Panel ──────────────────────────────────────────────────────────────────
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) as cnt FROM registrations")
    total_reg = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) as cnt FROM attendance WHERE att_date=%s", (date.today(),))
    today_att = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) as cnt FROM courses")
    total_courses = cur.fetchone()['cnt']

    cur.execute(
        """SELECT r.*, c.course_name FROM registrations r
           JOIN courses c ON r.course_id = c.id
           ORDER BY r.registered_on DESC LIMIT 10"""
    )
    recent_regs = cur.fetchall()

    cur.execute(
        """SELECT a.*, c.course_name FROM attendance a
           JOIN courses c ON a.course_id = c.id
           WHERE a.att_date = %s ORDER BY a.marked_at DESC""",
        (date.today(),)
    )
    today_records = cur.fetchall()

    cur.execute(
        """SELECT c.course_name, COUNT(r.id) as count
           FROM courses c LEFT JOIN registrations r ON c.id = r.course_id
           GROUP BY c.id ORDER BY count DESC"""
    )
    course_stats = cur.fetchall()

    cur.close()
    return render_template('admin.html',
                           total_reg=total_reg,
                           today_att=today_att,
                           total_courses=total_courses,
                           recent_regs=recent_regs,
                           today_records=today_records,
                           course_stats=course_stats,
                           today=date.today())


@app.route('/admin/registrations')
def admin_registrations():
    cur = mysql.connection.cursor()
    cur.execute(
        """SELECT r.*, c.course_name FROM registrations r
           JOIN courses c ON r.course_id = c.id
           ORDER BY r.registered_on DESC"""
    )
    regs = cur.fetchall()
    cur.close()
    return render_template('admin_registrations.html', regs=regs)


@app.route('/admin/attendance')
def admin_attendance():
    filter_date = request.args.get('date', str(date.today()))
    cur = mysql.connection.cursor()
    cur.execute(
        """SELECT a.*, c.course_name FROM attendance a
           JOIN courses c ON a.course_id = c.id
           WHERE a.att_date = %s ORDER BY a.marked_at DESC""",
        (filter_date,)
    )
    records = cur.fetchall()
    cur.close()
    return render_template('admin_attendance.html', records=records, filter_date=filter_date)


# ── About ────────────────────────────────────────────────────────────────────────
@app.route('/about')
def about():
    return render_template('about.html')


# ── Contact ──────────────────────────────────────────────────────────────────────
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, subject, message]):
            flash('Please fill all fields.', 'error')
            return render_template('contact.html')

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO contact_messages (name, email, subject, message) VALUES (%s,%s,%s,%s)",
            (name, email, subject, message)
        )
        mysql.connection.commit()
        cur.close()
        flash('Message sent! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
