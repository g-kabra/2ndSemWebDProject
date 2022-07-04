from flask import Blueprint, render_template, redirect, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Student, Teacher, Admin
from flask_login import login_user, login_required, logout_user, current_user
from .main import profile
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('loginpage.html')

@auth.route('/signup', methods = ['POST', 'GET'])
@login_required
def signup():
    if (current_user.role == 'admin'):
        return render_template('signuppage.html')
    return profile()

@auth.route('/logout')
@login_required
def logout():
    print("logged out", current_user)
    logout_user()
    return render_template('loginpage.html')

@auth.route('/signup/student', methods=['POST'])
@login_required
def signupStudent():
    if (current_user.role == 'admin'):
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
    return profile()

@auth.route('/signup/teacher', methods=['POST'])
@login_required
def signupTeacher():
    if (current_user.role == 'admin'):
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        # rollno = request.form['rollno']
        
        teacher = Teacher.query.filter_by(email = email).first()
        
        if teacher:
            return "Kya be"
        
        new_user = Teacher(email = email, fname = fname, lname = lname, password = generate_password_hash(password, method='sha256'))
        
        db.session.add(new_user)
        db.session.commit()
        return redirect('/signup')
    return profile()

@auth.route('/signup/admin', methods=['POST'])
# @login_required
def signupAdmin():
    # if (current_user.role == 'admin'):
        fname = request.form['fname']
        lname = request.form['lname']
        dept = request.form['dept']
        designation = request.form['designation']
        email = request.form['email']
        password = request.form['password']
        
        admin = Admin.query.filter_by(email = email).first()
        
        if admin:
            return "Kya be"

        new_admin = Admin(email = email, fname = fname, lname = lname, dept = dept, designation = designation, password = generate_password_hash(password, method='sha256'))
        
        db.session.add(new_admin)
        db.session.commit()
        return redirect('/signup')
    # return profile()
    
@auth.route('/login/student', methods = ['POST'])
def loginStudent():
    email = request.form['email']
    password = request.form['password']
    
    student = Student.query.filter_by(email=email).first()
    
    if not student or not check_password_hash(student.password, password):
        return "Kya be"
    session['role'] = 'student'
    login_user(student)
    print("Logged in", current_user)
    return profile()

@auth.route('/login/teacher', methods = ['POST'])
def loginTeacher():
    email = request.form['email']
    password = request.form['password']
    
    teacher = Teacher.query.filter_by(email=email).first()
    
    if not teacher or not check_password_hash(teacher.password, password):
        return "Kya be"
    session['role'] = 'teacher'
    login_user(teacher)
    print("Logged in", current_user)
    return profile()

@auth.route('/login/admin', methods = ['POST'])
def loginAdmin():
    email = request.form['email']
    password = request.form['password']
    
    admin = Admin.query.filter_by(email=email).first()
    
    if not admin or not check_password_hash(admin.password, password):
        return "Kya be"
    
    
    session['role'] = 'admin'
    login_user(admin)
    print("Logged in", current_user)
    return profile()


