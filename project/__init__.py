from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    from .models import Student, Teacher, Admin
    
    loginUser = LoginManager(app)
    loginUser.login_view = 'auth.login'
    loginUser.init_app(app)
    
    @loginUser.user_loader
    def load_user(user_id):
        if 'role' in session:
            if(session['role'] == 'student'):
                return Student.query.get(int(user_id))
            elif(session['role'] == 'teacher'):
                return Teacher.query.get(int(user_id))
            elif(session['role'] == 'admin'):
                return Admin.query.get(int(user_id))
        return "Error"
    
    
    app.config['SECRET_KEY'] = 'very-secret-indeed'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .teacher import teacher as teacher_blueprint
    app.register_blueprint(teacher_blueprint)
    
    from .student import student as student_blueprint
    app.register_blueprint(student_blueprint)
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    return app 