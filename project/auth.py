from flask import Blueprint, render_template, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Student
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('loginpage.html')

@auth.route('/signup')
def signup():
    return render_template('signuppage.html')

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/signup/student', methods=['POST'])
def signupStudent():
    fname = request.form['fname']
    lname = request.form['lname']
    branch = request.form['branch']
    year = request.form['year']
    email = request.form['email']
    password = request.form['password']
    # rollno = request.form['rollno']
    
    student = Student.query.filter_by(email = email).first()
    
    if student:
        return "Kya be"
    
    new_user = Student(email = email, fname = fname, lname = lname, branch = branch, year = year, password = generate_password_hash(password, method='sha256'))
    
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
    
    return render_template('/student_profile.html', email = student.email, name = student.fname + " " + student.lname, branch = student.branch)