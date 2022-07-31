from flask import Blueprint, render_template, request, send_file, redirect
from flask_login import login_required, current_user
from .models import Student, Teacher, Assignments, Marks, Subject, Timetable, Grades
from .main import profile
from . import db
import pandas as pd

teacher = Blueprint('teacher', __name__)


@teacher.route('/teacher/enter_selection')
@login_required
def enter_selection():
    if(current_user.role == 'teacher'):
        assigned = Subject.query.filter_by(teacher_id=current_user.id)
        options = []
        for i in assigned:
            options.append(str(i.year) + " " +
                           str(i.semester) + " " + str(i.branch))
        return render_template('teacher_student_selector.html', options=options, link='/teacher/enter_marks')
    return profile()


@teacher.route('/teacher/enter_marks', methods=['POST'])
@login_required
def enter_marks():
    if(current_user.role == 'teacher'):
        choice = request.form["choice"]
        branch = choice[7:]
        year = int(choice[:4])
        semester = int(choice[5:6])
        students = Student.query.filter_by(branch=branch, year=year).all()
        subject = Subject.query.filter_by(
            branch=branch, year=year, teacher_id=current_user.id, semester=semester).first()
        if not subject:
            return render_template("Notice_Page.html", message="You don't have access to this class, please check your credentials.", back="/teacher/enter_selection")
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, semester=semester, subject=subject.subject).all()
        return render_template('teacher_table.html', students=students, assignments=assignments, branch=branch, year=year, subject=subject.subject, semester=semester)
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
            return render_template('Notice_Page.html', message="This assignment already exists.", back="/teacher/enter_selection")
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
        return render_template('teacher_table.html', students=students, assignments=assignments, branch=branch, year=year, subject=subject, semester=semester)
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
        results = []
        for i in students:
            if(Marks.query.filter_by(assignment_id=ass.id, rollno=i.rollno).first()):
                results.append((i, Marks.query.filter_by(
                    assignment_id=ass.id, rollno=i.rollno).first()))
            else:
                results.append((i, 0))
        return render_template('teacher_table.html', students=results, assignments=assignments, branch=branch, year=year, subject=subject, assignment=ass, semester=semester, maxmarks=ass.max_marks)
    return profile()


@teacher.route('/teacher/add_marks_template/<int:year>/<string:branch>/<string:subject>/<int:semester>/<string:assignment>', methods=['POST'])
@login_required
def add_marks_template(year, semester, subject, assignment, branch):
    if(current_user.role == 'teacher'):
        students = Student.query.filter_by(branch=branch, year=year).all()
        ass = Assignments.query.filter_by(
            year=year, branch=branch, subject=subject, assignment=assignment, semester=semester).first()
        keys = {"year": [], "branch": [], "subject": [],
                "semester": [], "assignment": [], "rollno": [], "name": [], "marks": [], "max marks": []}
        for stud in students:
            keys['year'].append(year)
            keys['branch'].append(branch)
            keys['subject'].append(subject)
            keys['semester'].append(semester)
            keys['assignment'].append(assignment)
            keys['rollno'].append(stud.rollno)
            keys['name'].append(stud.fname + " " + stud.lname)
            keys['marks'].append((Marks.query.filter_by(
                assignment_id=ass.id, rollno=stud.rollno).first()).marks)
            keys['max marks'].append(ass.max_marks)
        df = pd.DataFrame(data=keys)
        df.to_excel("./app/templates/test1.xlsx")
        return send_file("./templates/test1.xlsx", attachment_filename=assignment + " " + branch + " " + str(year) + ".xlsx")
    return profile()


@teacher.route("/teacher/add_marks_excel/<int:year>/<string:branch>/<string:subject>/<int:semester>/<string:assignment>", methods=['POST'])
@login_required
def add_marks_excel(year, subject, semester, assignment, branch):
    if(current_user.role == 'teacher'):
        information = request.files['excel-file']
        object = pd.read_excel(information)
        students = Student.query.filter_by(branch=branch, year=year).all()
        ass = Assignments.query.filter_by(
            year=year, branch=branch, subject=subject, assignment=assignment, semester=semester).first()
        for i in range(len(object[object.keys()[0]])):
            rollno = object.iloc[i]["rollno"]
            marks = object.iloc[i]["marks"]
            if not marks:
                marks = 0
            if(not str(marks).isnumeric() or marks > ass.max_marks):
                return "Please check the value entered at row number " + str(i+1)
            m = Marks.query.filter_by(
                assignment_id=ass.id, rollno=rollno).first()
            m.marks = int(marks)
        db.session.commit()
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, subject=subject, semester=semester).all()
        results = db.session.query(Student, Marks).join(Marks).filter(
            Student.branch == branch, Student.year == year, Marks.assignment_id == ass.id)
        relative_max = max([i[1].marks for i in results])
        return render_template('teacher_table_view.html', results=results, assignments=assignments, branch=branch, year=year, subject=subject, assignment=ass, semester=semester, relative_max=relative_max, round=round)
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
            if not stud:
                stud = 0
            marks = Marks.query.filter_by(
                assignment_id=ass.id, rollno=student.rollno).first()
            marks.marks = stud
            # print("Updated", stud, marks)
        db.session.commit()
        assignments = Assignments.query.filter_by(
            branch=branch, year=year, subject=subject, semester=semester).all()
        results = db.session.query(Student, Marks).join(Marks).filter(
            Student.branch == branch, Student.year == year, Marks.assignment_id == ass.id)
        relative_max = max([i[1].marks for i in results])
        return render_template('teacher_table_view.html', results=results, assignments=assignments, branch=branch, year=year, subject=subject, assignment=ass, semester=semester, relative_max=relative_max, round=round)
    return profile()


@teacher.route('/teacher/delete_assignment/<int:year>/<string:branch>/<string:subject>/<int:semester>/<string:assignment>', methods=["GET", "POST"])
def delete_assignment(year, branch, semester, assignment, subject):
    if (current_user.role == 'teacher'):
        ass = Assignments.query.filter_by(
            year=year, branch=branch, subject=subject, assignment=assignment, semester=semester).first()
        marks = Marks.query.filter_by(assignment_id=ass.id).all()
        for mark in marks:
            db.session.delete(mark)
        db.session.delete(ass)
        db.session.commit()
        return redirect("/teacher/enter_selection")
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
        relative_max = max([i for i in results[1].marks])
        return render_template('teacher_table_view.html', results=results, students=students, assignments=assignments, branch=branch, year=year, subject=subject, assignment=ass, semester=semester, relative_max=relative_max)
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
        return render_template('teacher_table.html', students=results, assignments=assignments, branch=branch, year=year, subject=subject, assignment=ass, semester=semester, maxmarks=ass.max_marks)
    return profile()


@teacher.route('/teacher/view_timetable')
def view_timetable():
    if (current_user.role == 'teacher'):
        Mon1 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Mon1).first()
        if not (Mon1 and Mon1.Mon1 == current_user.id):
            Mon1 = "Free"
        else:
            Mon1 = Mon1.branch + " " + \
                str(Mon1.year) + " " + str(Mon1.semester)
        Mon2 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Mon2).first()
        if not (Mon2 and Mon2.Mon2 == current_user.id):
            Mon2 = "Free"
        else:
            Mon2 = Mon2.branch + " " + \
                str(Mon2.year) + " " + str(Mon2.semester)
        Mon3 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Mon3).first()
        if not (Mon3 and Mon3.Mon3 == current_user.id):
            Mon3 = "Free"
        else:
            Mon3 = Mon3.branch + " " + \
                str(Mon3.year) + " " + str(Mon3.semester)
        Mon4 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Mon4).first()
        if not (Mon4 and Mon4.Mon4 == current_user.id):
            Mon4 = "Free"
        else:
            Mon4 = Mon4.branch + " " + \
                str(Mon4.year) + " " + str(Mon4.semester)
        Mon5 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Mon5).first()
        if not (Mon5 and Mon5.Mon5 == current_user.id):
            Mon5 = "Free"
        else:
            Mon5 = Mon5.branch + " " + \
                str(Mon5.year) + " " + str(Mon5.semester)
        Tue1 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Tue1).first()
        if not (Tue1 and Tue1.Tue1 == current_user.id):
            Tue1 = "Free"
        else:
            Tue1 = Tue1.branch + " " + \
                str(Tue1.year) + " " + str(Tue1.semester)
        Tue2 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Tue2).first()
        if not (Tue2 and Tue2.Tue2 == current_user.id):
            Tue2 = "Free"
        else:
            Tue2 = Tue2.branch + " " + \
                str(Tue2.year) + " " + str(Tue2.semester)
        Tue3 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Tue3).first()
        if not (Tue3 and Tue3.Tue3 == current_user.id):
            Tue3 = "Free"
        else:
            Tue3 = Tue3.branch + " " + \
                str(Tue3.year) + " " + str(Tue3.semester)
        Tue4 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Tue4).first()
        if not (Tue4 and Tue4.Tue4 == current_user.id):
            Tue4 = "Free"
        else:
            Tue4 = Tue4.branch + " " + \
                str(Tue4.year) + " " + str(Tue4.semester)
        Tue5 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Tue5).first()
        if not (Tue5 and Tue5.Tue5 == current_user.id):
            Tue5 = "Free"
        else:
            Tue5 = Tue5.branch + " " + \
                str(Tue5.year) + " " + str(Tue5.semester)
        Wed1 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Wed1).first()
        if not (Wed1 and Wed1.Wed1 == current_user.id):
            Wed1 = "Free"
        else:
            Wed1 = Wed1.branch + " " + \
                str(Wed1.year) + " " + str(Wed1.semester)
        Wed2 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Wed2).first()
        if not (Wed2 and Wed2.Wed2 == current_user.id):
            Wed2 = "Free"
        else:
            Wed2 = Wed2.branch + " " + \
                str(Wed2.year) + " " + str(Wed2.semester)
        Wed3 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Wed3).first()
        if not (Wed3 and Wed3.Wed3 == current_user.id):
            Wed3 = "Free"
        else:
            Wed3 = Wed3.branch + " " + \
                str(Wed3.year) + " " + str(Wed3.semester)
        Wed4 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Wed4).first()
        if not (Wed4 and Wed4.Wed4 == current_user.id):
            Wed4 = "Free"
        else:
            Wed4 = Wed4.branch + " " + \
                str(Wed4.year) + " " + str(Wed4.semester)
        Wed5 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Wed5).first()
        if not (Wed5 and Wed5.Wed5 == current_user.id):
            Wed5 = "Free"
        else:
            Wed5 = Wed5.branch + " " + \
                str(Wed5.year) + " " + str(Wed5.semester)
        Thu1 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Thu1).first()
        if not (Thu1 and Thu1.Thu1 == current_user.id):
            Thu1 = "Free"
        else:
            Thu1 = Thu1.branch + " " + \
                str(Thu1.year) + " " + str(Thu1.semester)
        Thu2 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Thu2).first()
        if not (Thu2 and Thu2.Thu2 == current_user.id):
            Thu2 = "Free"
        else:
            Thu2 = Thu2.branch + " " + \
                str(Thu2.year) + " " + str(Thu2.semester)
        Thu3 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Thu3).first()
        if not (Thu3 and Thu3.Thu3 == current_user.id):
            Thu3 = "Free"
        else:
            Thu3 = Thu3.branch + " " + \
                str(Thu3.year) + " " + str(Thu3.semester)
        Thu4 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Thu4).first()
        if not (Thu4 and Thu4.Thu4 == current_user.id):
            Thu4 = "Free"
        else:
            Thu4 = Thu4.branch + " " + \
                str(Thu4.year) + " " + str(Thu4.semester)
        Thu5 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Thu5).first()
        if not (Thu5 and Thu5.Thu5 == current_user.id):
            Thu5 = "Free"
        else:
            Thu5 = Thu5.branch + " " + \
                str(Thu5.year) + " " + str(Thu5.semester)
        Fri1 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Fri1).first()
        if not (Fri1 and Fri1.Fri1 == current_user.id):
            Fri1 = "Free"
        else:
            Fri1 = Fri1.branch + " " + \
                str(Fri1.year) + " " + str(Fri1.semester)
        Fri2 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Fri2).first()
        if not (Fri2 and Fri2.Fri2 == current_user.id):
            Fri2 = "Free"
        else:
            Fri2 = Fri2.branch + " " + \
                str(Fri2.year) + " " + str(Fri2.semester)
        Fri3 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Fri3).first()
        if not (Fri3 and Fri3.Fri3 == current_user.id):
            Fri3 = "Free"
        else:
            Fri3 = Fri3.branch + " " + \
                str(Fri3.year) + " " + str(Fri3.semester)
        Fri4 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Fri4).first()
        if not (Fri4 and Fri4.Fri4 == current_user.id):
            Fri4 = "Free"
        else:
            Fri4 = Fri4.branch + " " + \
                str(Fri4.year) + " " + str(Fri4.semester)
        Fri5 = db.session.query(Timetable).join(
            Subject, Subject.teacher_id == Timetable.Fri5).first()
        if not (Fri5 and Fri5.Fri5 == current_user.id):
            Fri5 = "Free"
        else:
            Fri5 = Fri5.branch + " " + \
                str(Fri5.year) + " " + str(Fri5.semester)
        return render_template('StudentTimetable.html', Mon1=Mon1, Mon2=Mon2, Mon3=Mon3, Mon4=Mon4, Mon5=Mon5, Tue1=Tue1, Tue2=Tue2, Tue3=Tue3, Tue4=Tue4, Tue5=Tue5, Wed1=Wed1, Wed2=Wed2, Wed3=Wed3, Wed4=Wed4, Wed5=Wed5, Thu1=Thu1, Thu2=Thu2, Thu3=Thu3, Thu4=Thu4, Thu5=Thu5, Fri1=Fri1, Fri2=Fri2, Fri3=Fri3, Fri4=Fri4, Fri5=Fri5, teacher = True)
    return profile()


@teacher.route('/teacher/grades_student_select')
def grades_student_select():
    if (current_user.role == 'teacher'):
        assigned = Subject.query.filter_by(teacher_id=current_user.id)
        options = []
        for i in assigned:
            options.append(str(i.year) + " " +
                           str(i.semester) + " " + str(i.branch))
        return render_template('teacher_student_selector.html', link="/teacher/enter_grades", options=options)
    return profile()


@teacher.route('/teacher/enter_grades', methods=['POST'])
def enter_grades():
    if (current_user.role == 'teacher'):
        choice = request.form["choice"]
        branch = choice[7:]
        year = int(choice[:4])
        semester = int(choice[5:6])
        return render_template('grades.html', branch=branch, year=year, semester=semester)
    return profile()


@teacher.route('/teacher/add_grades/<string:branch>/<int:year>/<int:semester>', methods=['POST'])
def add_grades(branch, year, semester):
    if (current_user.role == 'teacher'):
        aplus = request.form['A+']
        a = request.form['A']
        b = request.form['B']
        c = request.form['C']
        f = 0
        subject = Subject.query.filter_by(
            semester=semester, branch=branch, year=year, teacher_id=current_user.id).first().subject
        grade = Grades.query.filter_by(
            branch=branch, year=year, semester=semester, subject=subject, teacher_id=current_user.id).first()
        if grade:
            db.session.delete(grade)
            db.session.commit()
        grade = Grades(A1=aplus, A=a, B=b, C=c, F=f,
                       branch=branch, year=year, semester=semester, subject=subject, teacher_id=current_user.id)
        db.session.add(grade)
        db.session.commit()
        ass = Assignments.query.filter_by(
            branch=branch, year=year, semester=semester).all()
        studs = Student.query.filter_by(branch=branch, year=year).all()
        marks = []
        grade = Grades.query.filter_by(
            branch=branch, year=year, semester=semester, subject=subject, teacher_id=current_user.id).first()
        for stud in studs:
            mark = []
            mark.append(stud.rollno)
            mark.append(stud.fname + " " + stud.lname)
            for i in ass:
                mark.append(Marks.query.filter_by(
                    rollno=stud.rollno, assignment_id=i.id).first().marks)
            mark.append(sum(mark[2:]))
            if(mark[-1] >= grade.A1):
                mark.append("A+")
            elif(mark[-1] >= grade.A):
                mark.append("A")
            elif(mark[-1] >= grade.B):
                mark.append("B")
            elif(mark[-1] >= grade.C):
                mark.append("C")
            else:
                mark.append("F")
            marks.append(mark)
        return render_template('teacher_marksheet.html', assignments=ass, marks=marks)
    return profile()


@teacher.route('/teacher/view_grade_selector')
def view_grade_selector():
    if current_user.role == 'teacher':
        assigned = Grades.query.filter_by(teacher_id=current_user.id).all()
        options = []
        for i in assigned:
            print(i)
            options.append(str(i.year) + " " +
                           str(i.semester) + " " + str(i.branch))
        return render_template('teacher_student_selector.html', options=options, link="/teacher/view_grades")
    return profile()


@teacher.route('/teacher/view_grades', methods=['GET', 'POST'])
def teacher_view_grades():
    if current_user.role == 'teacher':
        choice = request.form["choice"]
        branch = choice[7:]
        year = int(choice[:4])
        semester = int(choice[5:6])
        subject = Subject.query.filter_by(
            semester=semester, branch=branch, year=year, teacher_id=current_user.id).first().subject
        ass = Assignments.query.filter_by(
            branch=branch, year=year, semester=semester).all()
        studs = Student.query.filter_by(branch=branch, year=year).all()
        marks = []
        grade = Grades.query.filter_by(
            branch=branch, year=year, semester=semester, subject=subject).first()
        for stud in studs:
            mark = []
            mark.append(stud.rollno)
            mark.append(stud.fname + " " + stud.lname)
            for i in ass:
                mark.append(Marks.query.filter_by(
                    rollno=stud.rollno, assignment_id=i.id).first().marks)
            mark.append(sum(mark[2:]))
            if(mark[-1] >= grade.A1):
                mark.append("A+")
            elif(mark[-1] >= grade.A):
                mark.append("A")
            elif(mark[-1] >= grade.B):
                mark.append("B")
            elif(mark[-1] >= grade.C):
                mark.append("C")
            else:
                mark.append("F")
            marks.append(mark)
        return render_template('teacher_marksheet.html', assignments=ass, marks=marks)
    return profile()
