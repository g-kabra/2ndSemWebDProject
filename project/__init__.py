from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    loginStudent = LoginManager(app)
    loginStudent.login_view = 'auth.login'
    loginStudent.init_app(app)
    
    from .models import Student, Teacher
    
    @loginStudent.user_loader
    def load_student(student_id):
        return Student.query.get(int(student_id))
    
    loginTeacher = LoginManager(app)
    loginTeacher.login_view = 'auth.login'
    loginTeacher.init_app(app)
    
    @loginTeacher.user_loader
    def load_teacher(teacher_id):
        return Teacher.query.get(int(teacher_id))
    
    app.config['SECRET_KEY'] = 'very-secret-indeed'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
    
    db.init_app(app)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .teacher import teacher as teacher_blueprint
    app.register_blueprint(teacher_blueprint)
    
    return app 