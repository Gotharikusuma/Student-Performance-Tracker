Student Performance Tracker
Overview

Student Performance Tracker is a web-based application developed using Python Flask and SQLite. The application helps teachers manage student records, track subject-wise marks, calculate average scores, and monitor student performance through a simple and user-friendly interface.

Features
- Add new students
- Edit student details
- Delete student records
- Add subject-wise marks
- View student performance details
- Calculate average marks
- Search students by name
- Dashboard with statistics
- SQLite database integration
- Responsive user interface using Bootstrap

Technologies Used
- Python
- Flask
- SQLite
- HTML
- CSS
- Bootstrap

Project Structure

Student-Performance-Tracker/

├── app.py

├── students.db

├── requirements.txt

├── Procfile

├── templates/

│ ├── base.html

│ ├── home.html

│ ├── add_student.html

│ ├── edit_student.html

│ ├── add_marks.html

│ ├── view_students.html

│ ├── student_detail.html

│ └── charts.html

Installation
Clone the repository

git clone https://github.com/Gotharikusuma/Student-Performance-Tracker.git

Navigate to the project directory

cd Student-Performance-Tracker

Install dependencies

pip install -r requirements.txt

Run the application

python app.py

Open your browser and visit the generated local URL

Example:
http://127.0.0.1:8000