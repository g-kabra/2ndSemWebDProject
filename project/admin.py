from flask import Blueprint, render_template, request, session, flash
from flask_login import login_required, current_user
from .models import Student, Teacher, Assignments, Marks, Admin, Subject, Timetable
from .main import profile
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/admin/teacher_assign')
@login_required
def teacher_assign():
    if session['role'] == 'admin':
        teachers = Teacher.query.all()
        return render_template('admin_student_selector.html', teachers = teachers, added = 0)
    return profile()

@admin.route('/admin/teacher_assign/selected', methods = ['POST'])
@login_required
def teacher_assigned():
    if session['role'] == 'admin':
        teachers = Teacher.query.all()
        teacher_id = request.form['teacher']
        year = request.form['year']
        branch = request.form['branch']
        semester = request.form['semester']
        subject = request.form['subject']
        sub = Subject.query.filter_by(subject=subject, year=year, branch=branch, semester=semester).first()
        if sub:
            sub.teacher_id = teacher_id
        else:
            sub = Subject(subject=subject, year=year, branch=branch, semester=semester, teacher_id = teacher_id)
            db.session.add(sub)
            db.session.commit()
        return render_template('admin_student_selector.html', added = 1, teachers = teachers)
    return profile()

@admin.route('/admin/timetable', methods = ['POST', 'GET'])
@login_required
def timetable_choose():
    print(session['role'])
    if session['role'] == 'admin':
        return render_template('admin_student_selector.html', timetable = 1)
    return profile()

@admin.route('/admin/timetable/selected', methods = ['POST'])
@login_required
def timetable_assign():
    if session['role'] == 'admin':
        year = request.form['year']
        branch = request.form['branch']
        semester = request.form['semester']
        results = db.session.query(Subject, Teacher).join(Teacher).filter(
            Subject.branch == branch, Subject.year == year, Subject.semester == semester).all()
        return render_template('AdminTimetable.html', results = results, branch = branch, year = year, semester = semester)
    return profile()

@admin.route('/admin/add_timetable/<string:branch>/<int:year>/<int:semester>', methods = ['POST', 'GET'])
@login_required
def add_timetable(branch, year, semester):
    if session['role'] == 'admin':
        Mon1 = request.form['Mon1']
        Mon2 = request.form['Mon2']
        Mon3 = request.form['Mon3']
        Mon4 = request.form['Mon4']
        Mon5 = request.form['Mon5']
        Tue1 = request.form['Tue1']
        Tue2 = request.form['Tue2']
        Tue3 = request.form['Tue3']
        Tue4 = request.form['Tue4']
        Tue5 = request.form['Tue5']
        Wed1 = request.form['Wed1']
        Wed2 = request.form['Wed2']
        Wed3 = request.form['Wed3']
        Wed4 = request.form['Wed4']
        Wed5 = request.form['Wed5']
        Thu1 = request.form['Thu1']
        Thu2 = request.form['Thu2']
        Thu3 = request.form['Thu3']
        Thu4 = request.form['Thu4']
        Thu5 = request.form['Thu5']
        Fri1 = request.form['Fri1']
        Fri2 = request.form['Fri2']
        Fri3 = request.form['Fri3']
        Fri4 = request.form['Fri4']
        Fri5 = request.form['Fri5']
        tt = Timetable.query.filter_by(branch=branch, year=year, semester=semester).first()
        if tt:
            db.session.delete(tt)
            db.session.commit()
        tt = Timetable(branch = branch, year = year, semester = semester, Mon1 = Mon1, Mon2 = Mon2, Mon3 = Mon3, Mon4 = Mon4,Mon5 = Mon5, Tue1 = Tue1, Tue2 = Tue2, Tue3 = Tue3, Tue4 = Tue4, Tue5 = Tue5, Wed1 = Wed1, Wed2 = Wed2, Wed3 = Wed3, Wed4 = Wed4, Wed5 = Wed5, Thu1 = Thu1, Thu2 = Thu2, Thu3 = Thu3, Thu4 = Thu4, Thu5 = Thu5, Fri1 = Fri1, Fri2 = Fri2, Fri3 = Fri3, Fri4 = Fri4, Fri5 = Fri5)
        db.session.add(tt)
        db.session.commit()
    return profile()