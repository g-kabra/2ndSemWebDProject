from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Student, Teacher, Assignments, Marks
from .main import profile
from . import db

teacher = Blueprint('teacher', __name__)

@teacher.route('/teacher/enter_selection')
@login_required
def enter_selection():
    if(current_user.role == 'teacher'):
        return render_template('teacher_student_selector.html')
    return profile()
@teacher.route('/teacher/enter_marks', methods=['POST'])
@login_required
def enter_marks():
    if(current_user.role == 'teacher'):
        branch = request.form['branch']
        year = request.form['year']
        students = Student.query.filter_by(branch=branch, year = year).all()
        assignments = Assignments.query.filter_by(branch=branch, year = year).all()
        return render_template('teacher_table.html', students = students, assignments = assignments, branch = branch, year = year, subject = current_user.subject)
    return profile()
    
@teacher.route('/teacher/add_assignment/', methods = ['POST'])
@login_required
def add_assignment():
    if (current_user.role == 'teacher'):
        year = request.form['year']
        branch = request.form['branch']
        subject = request.form['subject']
        assignment = request.form['assignment']
        max_marks = request.form['maxmarks']
        
        ass = Assignments.query.filter_by(assignment = assignment).first()
        
        if ass:
            return "Kya be"
        
        new_ass = Assignments(year = year, branch = branch, subject = subject, assignment = assignment, max_marks = max_marks)
        db.session.add(new_ass)
        db.session.commit()
        assignments = Assignments.query.filter_by(branch=branch, year = year).all()
        students = Student.query.filter_by(branch=branch, year=year)
        return render_template('teacher_table.html', students = students, assignments = assignments, branch = branch, year = year, subject = current_user.subject)
    return profile()

@teacher.route('/teacher/assignment_selected/<int:year>/<string:branch>/<string:subject>/', methods=['POST'])
@login_required
def assignment_selected(year, branch, subject):
    if (current_user.role == 'teacher'):
        assignment = request.form['assignment']
        students = Student.query.filter_by(branch=branch, year=year).all()
        assignments = Assignments.query.filter_by(branch=branch, year = year, subject = subject).all()
        ass = Assignments.query.filter_by(year=year, branch=branch, subject=subject, assignment=assignment).first()
        return render_template('teacher_table.html', students = students, assignments = assignments, branch = branch, year = year, subject = current_user.subject, assignment = ass)
    return profile()

@teacher.route('/teacher/add_marks/<int:year>/<string:branch>/<string:subject>/<string:assignment>', methods=['POST'])
def add_marks(year, branch, subject, assignment):
    if(current_user.role == 'teacher'):
        students = Student.query.filter_by(branch=branch, year=year).all()
        # return branch
        
        ass = Assignments.query.filter_by(year=year, branch=branch, subject=subject, assignment=assignment).first()
        for student in students:
            marks = request.form[student.rollno]
            new_marks = Marks(assignment=assignment, marks=marks, rollno = student.rollno, assignment_id = ass.id)
            db.session.add(new_marks)
            db.session.commit()
        assignments = Assignments.query.filter_by(branch=branch, year = year, subject = subject).all()
        results = db.session.query(Student, Marks).join(Marks).filter(Student.branch==branch, Student.year==year)
        # return str(results)
        return render_template('teacher_table_view.html', results=results, students = students, assignments = assignments, branch = branch, year = year, subject = current_user.subject, assignment = ass)
    return profile()
    
@teacher.route('/teacher/view_marks/<int:year>/<string:branch>/<string:subject>/<string:assignment>', methods=['GET','POST'])
def view_marks(year, branch, subject, assignment):
    if(current_user.role == 'teacher'):
        students = Student.query.filter_by(branch=branch, year=year).all()
        ass = Assignments.query.filter_by(year=year, branch=branch, subject=subject, assignment=assignment).first()
        assignments = Assignments.query.filter_by(branch=branch, year = year, subject=subject).all()
        results = db.session.query(Student, Marks).join(Marks).all()
        return render_template('teacher_table_view.html', results=results, students = students, assignments = assignments, branch = branch, year = year, subject = current_user.subject, assignment = ass)
    return profile()