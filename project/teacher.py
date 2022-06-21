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
        semester = request.form['semester']
        students = Student.query.filter_by(branch=branch, year=year).all()
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, semester=semester).all()
        return render_template('teacher_table.html', students=students, assignments=assignments, branch=branch, year=year, subject="DS", semester=semester)
    return profile()


@teacher.route('/teacher/add_assignment', methods=['POST'])
@login_required
def add_assignment():
    if (current_user.role == 'teacher'):
        year = request.form['year']
        branch = request.form['branch']
        subject = request.form['subject']
        semester = request.form['semester']
        assignment = request.form['assignment']
        max_marks = request.form['maxmarks']

        ass = Assignments.query.filter_by(
            assignment=assignment, branch=branch, subject=subject, year=year, semester=semester).first()
        students = Student.query.filter_by(branch=branch, year=year)
        if ass:
            return "Kya be"
        new_ass = Assignments(year=year, branch=branch, subject=subject,
                              assignment=assignment, max_marks=max_marks, semester=semester)
        db.session.add(new_ass)
        db.session.commit()
        ass = Assignments.query.filter_by(
            assignment=assignment, branch=branch, subject=subject, year=year, semester=semester).first()
        for student in students:
            marks = Marks(assignment_id=ass.id,
                          rollno=student.rollno, assignment=ass.assignment)
            db.session.add(marks)
        db.session.commit()
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, semester=semester).all()
        return render_template('teacher_table.html', students=students, assignments=assignments, branch=branch, year=year, subject="DS", semester=semester)
    return profile()


@teacher.route('/teacher/assignment_selected/<int:year>/<string:branch>/<int:semester>/<string:subject>', methods=['POST'])
@login_required
def assignment_selected(year, branch, subject, semester):
    if (current_user.role == 'teacher'):
        assignment = request.form['assignment']
        students = Student.query.filter_by(branch=branch, year=year).all()
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, subject=subject, semester=semester).all()
        ass = Assignments.query.filter_by(
            year=year, branch=branch, subject=subject, assignment=assignment, semester=semester).first()
        results = db.session.query(Student, Marks).join(Marks).filter(
            Student.branch == branch, Student.year == year, Marks.assignment_id == ass.id).all()
        for a in results:
            print(a)
        return render_template('teacher_table.html', students=results, assignments=assignments, branch=branch, year=year, subject="DS", assignment=ass, semester=semester)
    return profile()


@teacher.route('/teacher/add_marks/<int:year>/<string:branch>/<string:subject>/<int:semester>/<string:assignment>', methods=['POST'])
@login_required
def add_marks(year, branch, subject, assignment, semester):
    if(current_user.role == 'teacher'):
        students = Student.query.filter_by(branch=branch, year=year).all()
        ass = Assignments.query.filter_by(
            year=year, branch=branch, subject=subject, assignment=assignment, semester=semester).first()
        for student in students:
            stud = request.form[student.rollno]
            marks = Marks.query.filter_by(
                assignment_id=ass.id, rollno=student.rollno).first()
            marks.marks = stud
            print("Updated", stud, marks)
        db.session.commit()
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, subject=subject, semester=semester).all()
        results = db.session.query(Student, Marks).join(Marks).filter(
            Student.branch == branch, Student.year == year, Marks.assignment_id == ass.id)
        return render_template('teacher_table_view.html', results=results, assignments=assignments, branch=branch, year=year, subject="DS", assignment=ass, semester=semester)
    return profile()


@teacher.route('/teacher/view_marks/<int:year>/<string:branch>/<string:subject>/<int:semester>/<string:assignment>', methods=['GET', 'POST'])
def view_marks(year, branch, subject, assignment, semester):
    if(current_user.role == 'teacher'):
        students = Student.query.filter_by(branch=branch, year=year).all()
        ass = Assignments.query.filter_by(
            year=year, branch=branch, subject=subject, assignment=assignment, semester=semester).first()
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, subject=subject, semester=semester).all()
        results = db.session.query(Student, Marks).join(Marks).filter(
            Student.branch == branch, Student.year == year, Marks.assignment_id == ass.id).all()
        return render_template('teacher_table_view.html', results=results, students=students, assignments=assignments, branch=branch, year=year, subject="DS", assignment=ass, semester=semester)
    return profile()


@teacher.route('/teacher/edit_marks/<int:year>/<string:branch>/<string:subject>/<int:semester>/<string:assignment>', methods=['POST'])
def edit_marks(year, branch, semester, subject, assignment):
    if (current_user.role == 'teacher'):
        students = Student.query.filter_by(branch=branch, year=year).all()
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, subject=subject, semester=semester).all()
        ass = Assignments.query.filter_by(
            year=year, branch=branch, subject=subject, assignment=assignment, semester=semester).first()
        results = db.session.query(Student, Marks).join(Marks).filter(
            Student.branch == branch, Student.year == year, Marks.assignment_id == ass.id).all()
        for a in results:
            print(a)
        return render_template('teacher_table.html', students=results, assignments=assignments, branch=branch, year=year, subject="DS", assignment=ass, semester=semester)
    return profile()