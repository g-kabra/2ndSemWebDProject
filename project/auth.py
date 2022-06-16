from flask import Blueprint, render_template, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Student, Teacher
from flask_login import login_user, login_required, logout_user
from .teacher import enterMarks
from .main import profile
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('loginpage.html')

@auth.route('/signup')
def signup():
    return render_template('signuppage.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('loginpage.html')

@auth.route('/signup/student', methods=['POST'])
def signupStudent():
    fname = request.form['fname']
    lname = request.form['lname']
    branch = request.form['branch']
    year = request.form['year']
    email = request.form['email']
    password = request.form['password']
    rollno = request.form['rollno']
    
    student = Student.query.filter_by(email = email).first()
    
    if student:
        return "Kya be"
    
    new_user = Student(email = email, fname = fname, lname = lname, branch = branch, year = year, password = generate_password_hash(password, method='sha256'), rollno = rollno)
    
    db.session.add(new_user)
    db.session.commit()
    return redirect('/signup')

@auth.route('/signup/teacher', methods=['POST'])
def signupTeacher():
    fname = request.form['fname']
    lname = request.form['lname']
    subject = request.form['subject']
    email = request.form['email']
    password = request.form['password']
    # rollno = request.form['rollno']
    
    teacher = Teacher.query.filter_by(email = email).first()
    
    if teacher:
        return "Kya be"
    
    new_user = Teacher(email = email, fname = fname, lname = lname, subject = subject, password = generate_password_hash(password, method='sha256'))
    
    db.session.add(new_user)
    db.session.commit()
    return redirect('/signup')

@auth.route('/login/student', methods = ['POST'])
def loginStudent():
    email = request.form['email']
    password = request.form['password']
    
    student = Student.query.filter_by(email=email).first()
    
    if not student or not check_password_hash(student.password, password):
        return "Kya be"
    login_user(student)
    return profile(student)

@auth.route('/login/teacher', methods = ['POST'])
def loginTeacher():
    email = request.form['email']
    password = request.form['password']
    
    teacher = Teacher.query.filter_by(email=email).first()
    
    if not teacher or not check_password_hash(teacher.password, password):
        return "Kya be"
    login_user(teacher)
    return profile(teacher)


