from flask import Blueprint, render_template
from flask_login import login_required, current_user

from project.teacher import enterMarks
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return profile(current_user)
    return render_template('loginpage.html')

@main.route('/profile')
@login_required
def profile(user):
    if(user.role == 'student'):
        return render_template('student_profile.html', email = current_user.email, name = current_user.fname + " " + current_user.lname, branch = current_user.branch)
    if(user.role == 'teacher'):
        return render_template('teacher_profile.html', email = current_user.email, name = current_user.fname + " " + current_user.lname, subject = current_user.subject)
    
@main.route('/enter_marks')
@login_required
def enter_marks():
    return enterMarks(current_user)