from email import message
from flask import Blueprint, render_template, redirect, request, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Student, Teacher, Admin
from flask_login import login_user, login_required, logout_user, current_user
from .main import profile
from . import db
import pandas as pd

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('loginpage.html')


@auth.route('/signup', methods=['POST', 'GET'])
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
        force = (request.form.get('force'))
        student = Student.query.filter_by(email=email).first()

        if student and not force:
            return render_template('Notice_page.html', message = "This student has already been registered.", override = "", back = "/signup")
        if student and force:
            db.session.delete(student)
            db.session.commit()

        new_user = Student(email=email, fname=fname, lname=lname, branch=branch, year=year,
                           password=generate_password_hash(password, method='sha256'), rollno=rollno)

        db.session.add(new_user)
        db.session.commit()
        return redirect('/signup')
    return profile()

@auth.route('/signup/student-signup-excel', methods=['POST'])
def admin_student_signup_excel():
    information = request.files['excel-file']
    object = pd.read_excel(information)
    for i in range(len(object[object.keys()[0]])):
        # print(object.iloc[i])
        email = object.iloc[i]["email"]
        fname = object.iloc[i]["fname"]
        lname = object.iloc[i]["lname"]
        branch = object.iloc[i]["branch"]
        year = int(object.iloc[i]["year"])
        print(year)
        password = object.iloc[i]["password"]
        print(password)
        rollno = object.iloc[i]["rollno"]
        student = Student.query.filter_by(email=email).first()

        if student:
            db.session.delete(student)
            db.session.commit()
        new_user = Student(email=email, fname=fname, lname=lname, branch=branch, year=year,
                           password=generate_password_hash(password, method='sha256'), rollno=rollno)
        db.session.add(new_user)
    db.session.commit()
    return profile()

@auth.route('/signup/student-signup-excel-download', methods=['POST'])
def admin_student_signup_download():
    keys = {"email": [], "rollno": [], "fname": [],"lname": [],"branch": [],"year": [],"password": [] }
    df = pd.DataFrame(data=keys)
    df.to_excel("./app/templates/test1.xlsx")
    # print(df)
    return send_file("./templates/test1.xlsx", attachment_filename='signup_template.xlsx')

@auth.route('/signup/teacher', methods=['POST'])
@login_required
def signupTeacher():
    if (current_user.role == 'admin'):
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        # rollno = request.form['rollno']
        force = request.form.get('force')
        teacher = Teacher.query.filter_by(email=email).first()
        if teacher and not force:
            return render_template('Notice_page.html', message="This email has already been used. If you'd like to update the details, please use the checkbox", back = "/signup")
            # action: override
        if teacher and force:
            db.session.delete(teacher)
            db.session.commit()
        new_user = Teacher(email=email, fname=fname, lname=lname,
                           password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        return redirect('/signup')
    return profile()


@auth.route('/signup/admin', methods=['POST'])
@login_required
def signupAdmin():
    if (current_user.role == 'admin'):
        fname = request.form['fname']
        lname = request.form['lname']
        dept = request.form['dept']
        designation = request.form['designation']
        email = request.form['email']
        password = request.form['password']
        force = request.form.get('force')
        admin = Admin.query.filter_by(email=email).first()

        if admin and not force:
            return render_template('Notice_page.html', message="This email has already been used. If you'd like to update the details, please use the checkbox", back = "/signup")
            # action: override
        if admin and force:
            db.session.delete(admin)
            db.session.commit()
        new_admin = Admin(email=email, fname=fname, lname=lname, dept=dept,
                        designation=designation, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_admin)
        db.session.commit()
        return redirect('/signup')
    return profile()


@auth.route('/login/student', methods=['POST'])
def loginStudent():
    email = request.form['email']
    password = request.form['password']

    student = Student.query.filter_by(email=email).first()

    if not student or not check_password_hash(student.password, password):
        return render_template("Notice_page.html", message="Please check your login details.", back = "/login")
    session['role'] = 'student'
    login_user(student)
    print("Logged in", current_user)
    return profile()


@auth.route('/login/teacher', methods=['POST'])
def loginTeacher():
    email = request.form['email']
    password = request.form['password']

    teacher = Teacher.query.filter_by(email=email).first()

    if not teacher or not check_password_hash(teacher.password, password):
        return render_template("Notice_page.html", message="Please check your login details.", back = "/login")
    session['role'] = 'teacher'
    login_user(teacher)
    print("Logged in", current_user)
    return profile()


@auth.route('/login/admin', methods=['POST'])
def loginAdmin():
    email = request.form['email']
    password = request.form['password']

    admin = Admin.query.filter_by(email=email).first()

    if not admin or not check_password_hash(admin.password, password):
        return render_template("Notice_page.html", message="Please check your login details.", back = "/login")
    session['role'] = 'admin'
    login_user(admin)
    print("Logged in", current_user)
    return profile()
