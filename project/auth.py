from flask import Blueprint, redirect, url_for, request, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return redirect('/')

@auth.route('/signup')
def signup():
    return redirect('/')

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/signup/student/', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(email = email).first()
    
    if user:
        flash('Email Address already registered!')
    
    new_user = User(email=email, username=username, password=password)
    flash('Successfully registered')
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

# @auth.route('/login', methods=['POST'])
# def login():
#     email = request.form.get('email')
#     password = request.form.get('password')
    
#     user = User.query.filter_by(email = email).first()
    
#     if not user or not check_password_hash(user.password, password):
#         flash("Check your details and please try again.")
        
