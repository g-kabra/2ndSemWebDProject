from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Student, Teacher, Assignments, Marks
from . import db

student = Blueprint('student', __name__)

@student.route('/student/enter_selection', methods=['GET', 'POST'])
def enter_selection():
    rollno = current_user.rollno
    marks = db.session.query(Assignments, Marks).join(Assignments).filter(Marks.rollno == rollno).first()
    print(marks)
    return render_template('student_marks_view.html', marks = marks)

