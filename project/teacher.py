from flask import Blueprint, render_template, Markup
from flask_login import login_required, current_user
from .models import Student, Teacher
from . import db

teacher = Blueprint('teacher', __name__)

def enterMarks(user):
    if(user.role == 'student'):
        return render_template('student_profile.html', email = current_user.email, name = current_user.fname + " " + current_user.lname, branch = current_user.branch)
    students = Student.query.all()
    # printer = ""
    # for student in students:
    #     printer += student.fname
    # return printer
    return render_template('teacher_table.html', students = students)
