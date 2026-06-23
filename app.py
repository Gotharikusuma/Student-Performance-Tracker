from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DB_NAME = "students.db"

# ---------------- DB CONNECTION ----------------
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = user['username']
            return redirect('/')

        return "Invalid Username or Password"

    return render_template("login.html")
"""
# ---------------- HOME (DASHBOARD ONLY) ----------------
@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor()

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Total unique subjects
    cursor.execute("SELECT COUNT(DISTINCT subject) FROM marks")
    total_subjects = cursor.fetchone()[0]

    # Average marks
    cursor.execute("SELECT AVG(marks) FROM marks")
    avg_marks = cursor.fetchone()[0]

    conn.close()

    if avg_marks is None:
        avg_marks = 0
    else:
        avg_marks = round(avg_marks, 2)

    return render_template(
        "home.html",
        total_students=total_students,
        total_subjects=total_subjects,
        avg_marks=avg_marks
    )
    """
    conn = get_connection()
    cursor = conn.cursor()

    # total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # total marks entries
    cursor.execute("SELECT COUNT(*) FROM marks")
    total_marks = cursor.fetchone()[0]

    # average marks
    cursor.execute("SELECT AVG(marks) FROM marks")
    avg_marks = cursor.fetchone()[0]

    conn.close()

    if avg_marks is None:
        avg_marks = 0

    return render_template(
        "home.html",
        total_students=total_students,
        total_marks=total_marks,
        avg_marks=avg_marks
    )
"""

# ---------------- ADD STUDENT ----------------
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name'].strip()
        class_name = request.form['class'].strip()

        # Validate student name
        if not name.replace(" ", "").isalpha():
            return render_template(
                "add_student.html",
                message="Student name should contain only letters and spaces."
            )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO students (name, class) VALUES (?, ?)",
            (name, class_name)
        )

        conn.commit()
        conn.close()

        return redirect('/view_students')

    return render_template("add_student.html")

# ---------------- VIEW STUDENTS + SEARCH ----------------
@app.route('/view_students')
def view_students():
   
    search = request.args.get('search')

    conn = get_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute(
               "SELECT * FROM students WHERE name LIKE ? ORDER BY class ASC, name ASC",
               ('%' + search + '%',)
        )
    else:
        cursor.execute(
              "SELECT * FROM students ORDER BY class ASC, name ASC"
        )

    #students = cursor.fetchall()
    #conn.close()

    #return render_template(
     #   "view_students.html",
     #   students=students,
     #   search=search

    #)
    students = cursor.fetchall()
    conn.close()

    message = None

    if search and len(students) == 0:
        message = "No students found."

    return render_template(
         "view_students.html",
         students=students,
         search=search,
         message=message
    )
# ---------------- EDIT STUDENT ----------------
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        class_name = request.form['class']

        cursor.execute(
            "UPDATE students SET name=?, class=? WHERE id=?",
            (name, class_name, id)
        )

        conn.commit()
        conn.close()

        return redirect('/view_students')

    conn.close()

    return render_template("edit_student.html", student=student)

# ---------------- DELETE STUDENT ----------------
@app.route('/delete_student/<int:id>')
def delete_student(id):
   
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM marks WHERE student_id=?", (id,))
    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect('/view_students')

# ---------------- ADD MARKS ----------------
@app.route('/add_marks/<int:id>', methods=['GET', 'POST'])
def add_marks(id):

    if request.method == 'POST':

        subject = request.form['subject'].strip()
        marks = int(request.form['marks'])

        # Validate marks
        if marks < 0 or marks > 100:
            return "Marks must be between 0 and 100"

        conn = get_connection()
        cursor = conn.cursor()

        # Check duplicate subject for same student
        cursor.execute(
            "SELECT * FROM marks WHERE student_id=? AND LOWER(subject)=LOWER(?)",
            (id, subject)
        )

        existing = cursor.fetchone()

        if existing:
            conn.close()
            return "This subject already exists for this student."

        cursor.execute(
            "INSERT INTO marks (student_id, subject, marks) VALUES (?, ?, ?)",
            (id, subject, marks)
        )

        conn.commit()
        conn.close()

        return redirect('/view_students')

    return render_template("add_marks.html")
    """
    if request.method == 'POST':
        subject = request.form['subject']
        marks = request.form['marks']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO marks (student_id, subject, marks) VALUES (?, ?, ?)",
            (id, subject, int(marks))
        )

        conn.commit()
        conn.close()

        return redirect('/view_students')

    return render_template("add_marks.html")
"""
# ---------------- STUDENT PERFORMANCE ----------------
@app.route('/student/<int:id>')
def student_detail(id):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    cursor.execute("SELECT * FROM marks WHERE student_id=?", (id,))
    marks = cursor.fetchall()

    cursor.execute("SELECT AVG(marks) FROM marks WHERE student_id=?", (id,))
    avg = cursor.fetchone()[0]

    conn.close()

    if avg is None:
        avg = 0

    return render_template(
        "student_detail.html",
        student=student,
        marks=marks,
        avg=avg
    )

# ---------------- CHARTS ----------------
@app.route('/charts/<int:id>')
def charts(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    cursor.execute("SELECT subject, marks FROM marks WHERE student_id=?", (id,))
    data = cursor.fetchall()

    conn.close()

    subjects = [row['subject'] for row in data]
    marks = [row['marks'] for row in data]

    return render_template(
        "charts.html",
        student=student,
        subjects=subjects,
        marks=marks
    )

"""
@app.route('/search')
def search():
    query = request.args.get('query')

    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        (f"%{query}%",)
    )

    student = cursor.fetchone()
    conn.close()

    if student is None:
        return render_template(
            "students.html",
            student=None,
            message="No student found."
        )

    return render_template(
        "students.html",
        student=student,
        message=None
    )
"""
# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True,port=8000)