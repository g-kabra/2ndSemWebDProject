from crypt import methods
from locale import currency
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Student, Subject, Teacher, Assignments, Marks, Timetable, Notice
from .main import profile
import numpy as np
from . import db

student = Blueprint('student', __name__)


@student.route('/student/enter_selection', methods=['GET', 'POST'])
@login_required
def enter_selection():
    if(current_user.role == 'student'):
        marks = db.session.query(Assignments, Marks).join(
            Assignments).filter(Marks.rollno == current_user.rollno).all()
        results = []
        for i in marks:
            results.append([str(i[0].semester) + " " + str(i[0].subject)])
        results = np.array(results)
        results = np.unique(results)
        return render_template('student_sub_selector.html', results=results)
    return profile()


@student.route('/student/marks_selected', methods=['POST'])
@login_required
def show_marks():
    if(current_user.role == 'student'):
        response = request.form['subject']
        semester = response[0:1]
        subject = response[2:]
        marks = db.session.query(Assignments, Marks).join(Assignments).filter(
            Marks.rollno == current_user.rollno, Assignments.semester == semester, Assignments.subject == subject).all()
        return render_template('student_marks_view.html', marks=marks)
    return profile()


@student.route('/student/timetable', methods=['GET', 'POST'])
@login_required
def choose_timetable():
    if(current_user.role == 'student'):
        tts = db.session.query(Timetable).filter_by(
            branch=current_user.branch, year=current_user.year).all()
        return render_template('StudentTimetable.html', choose=True, tts=tts, student=True)
    return profile()


@student.route('/student/timetable/view', methods=['GET', 'POST'])
@login_required
def view_timetable():
    if current_user.role == 'student':
        semester = request.form['semester']
        tts = db.session.query(Timetable).filter_by(
            branch=current_user.branch, year=current_user.year).all()
        tt = db.session.query(Timetable).filter_by(
            branch=current_user.branch, year=current_user.year, semester=semester).first()
        if tt.Mon1 != 'free':
            Mon1 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Mon1).first().subject
        else:
            Mon1 = ""
        if tt.Mon2 != 'free':
            Mon2 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Mon2).first().subject
        else:
            Mon2 = ""
        if tt.Mon3 != 'free':
            Mon3 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Mon3).first().subject
        else:
            Mon3 = ""
        if tt.Mon4 != 'free':
            Mon4 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Mon4).first().subject
        else:
            Mon4 = ""
        if tt.Mon5 != 'free':
            Mon5 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Mon5).first().subject
        else:
            Mon5 = ""
        if tt.Tue1 != 'free':
            Tue1 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Tue1).first().subject
        else:
            Tue1 = ""
        if tt.Tue2 != 'free':
            Tue2 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Tue2).first().subject
        else:
            Tue2 = ""
        if tt.Tue3 != 'free':
            Tue3 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Tue3).first().subject
        else:
            Tue3 = ""
        if tt.Tue4 != 'free':
            Tue4 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Tue4).first().subject
        else:
            Tue4 = ""
        if tt.Tue5 != 'free':
            Tue5 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Tue5).first().subject
        else:
            Tue5 = ""
        if tt.Wed1 != 'free':
            Wed1 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Wed1).first().subject
        else:
            Wed1 = ""
        if tt.Wed2 != 'free':
            Wed2 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Wed2).first().subject
        else:
            Wed2 = ""
        if tt.Wed3 != 'free':
            Wed3 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Wed3).first().subject
        else:
            Wed3 = ""
        if tt.Wed4 != 'free':
            Wed4 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Wed4).first().subject
        else:
            Wed4 = ""
        if tt.Wed5 != 'free':
            Wed5 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Wed5).first().subject
        else:
            Wed5 = ""
        if tt.Thu1 != 'free':
            Thu1 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Thu1).first().subject
        else:
            Thu1 = ""
        if tt.Thu2 != 'free':
            Thu2 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Thu2).first().subject
        else:
            Thu2 = ""
        if tt.Thu3 != 'free':
            Thu3 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Thu3).first().subject
        else:
            Thu3 = ""
        if tt.Thu4 != 'free':
            Thu4 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Thu4).first().subject
        else:
            Thu4 = ""
        if tt.Thu5 != 'free':
            Thu5 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Thu5).first().subject
        else:
            Thu5 = ""
        if tt.Fri1 != 'free':
            Fri1 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Fri1).first().subject
        else:
            Fri1 = ""
        if tt.Fri2 != 'free':
            Fri2 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Fri2).first().subject
        else:
            Fri2 = ""
        if tt.Fri3 != 'free':
            Fri3 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Fri3).first().subject
        else:
            Fri3 = ""
        if tt.Fri4 != 'free':
            Fri4 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Fri4).first().subject
        else:
            Fri4 = ""
        if tt.Fri5 != 'free':
            Fri5 = db.session.query(Subject).filter_by(
                branch=current_user.branch, year=current_user.year, semester=semester, teacher_id=tt.Fri5).first().subject
        else:
            Fri5 = ""
        return render_template('StudentTimetable.html', Mon1=Mon1, Mon2=Mon2, Mon3=Mon3, Mon4=Mon4, Mon5=Mon5, Tue1=Tue1, Tue2=Tue2, Tue3=Tue3, Tue4=Tue4, Tue5=Tue5, Wed1=Wed1, Wed2=Wed2, Wed3=Wed3, Wed4=Wed4, Wed5=Wed5, Thu1=Thu1, Thu2=Thu2, Thu3=Thu3, Thu4=Thu4, Thu5=Thu5, Fri1=Fri1, Fri2=Fri2, Fri3=Fri3, Fri4=Fri4, Fri5=Fri5, choose=True, tts=tts, student=True)


@student.route('/student/notice')
def notice():
    notices = Notice.query.all()
    n = []
    l = 1
    for i in notices:
        n.append([l, i.heading, i.content])
        l += 1
    return render_template('notice_board.html', notices=n)
