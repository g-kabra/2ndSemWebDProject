from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Student, Teacher, Assignments, Marks, Admin
from .main import profile
from . import db

admin = Blueprint('admin', __name__)

