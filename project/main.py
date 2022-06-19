from flask import Blueprint, render_template, session
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if(current_user.is_authenticated):
        return profile()
    return render_template('loginpage.html')

@main.route('/profile')
def profile():
    print(current_user, "is logged in")
    if(session['role'] == 'student'):
        return render_template('student_profile.html', email = current_user.email, name = current_user.fname + " " + current_user.lname, branch = current_user.branch, rollno = current_user.rollno)
    if(session['role'] == 'teacher'):
        return render_template('teacher_profile.html', email = current_user.email, name = current_user.fname + " " + current_user.lname, subject = current_user.subject)
    if(session['role'] == 'admin'):
        return render_template('admin_profile.html', email = current_user.email, name = current_user.fname + " " + current_user.lname, dept = current_user.dept, designation = current_user.designation)
    return "F"
    