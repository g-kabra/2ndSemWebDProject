from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Student, Teacher, Assignments
from . import db

teacher = Blueprint('teacher', __name__)

@teacher.route('/enter_selection')
def enter_selection():
    if(current_user.role == 'student'):
        return render_template('student_profile.html', email = current_user.email, name = current_user.fname + " " + current_user.lname, branch = current_user.branch)
    return render_template('teacher_student_selector.html')

@teacher.route('/enter_marks', methods=['POST'])
def enter_marks():
    if(current_user.role == 'student'):
        return render_template('student_profile.html', email = current_user.email, name = current_user.fname + " " + current_user.lname, branch = current_user.branch)
    branch = request.form['branch']
    year = request.form['year']
    subject = current_user.subject
    students = Student.query.filter_by(branch=branch, year = year).all()
    assignments = Assignments.query.filter_by(branch=branch, year = year).all()
    return render_template('teacher_table.html', students = students, assignments = assignments, branch = branch, year = year, subject = current_user.subject)
    
@teacher.route('/teacher/add_assignment/<y>', methods = ['POST'])
def add_assignment(y):
    year = y
    branch = request.form['branch']
    subject = request.form['subject']
    assignment = request.form['assignment']
    max_marks = request.form['maxmarks']
    
    ass = Assignments.query.filter_by(assignment = assignment).first()
    
    if ass:
        return "Kya be"
    
    new_ass = Assignments(year = year, branch = branch, subject = subject, assignment = assignment, max_marks = max_marks)
    db.session.add(new_ass)
    db.session.commit()
    assignments = Assignments.query.filter_by(branch=branch, year = year).all()
    students = Student.query.filter_by(branch=branch, year=year)
    return render_template('teacher_table.html', students = students, assignments = assignments, branch = branch, year = year, subject = current_user.subject)
