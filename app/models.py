from . import db
from flask_login import UserMixin


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(4))
    type = db.Column(db.String(10))
    year_started = db.Column(db.Integer)
    
class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    rollno = db.Column(db.String(30))
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    branch = db.Column(db.String(4), db.ForeignKey('branch.branch'))
    year = db.Column(db.Integer)
    password = db.Column(db.String(30))
    role = db.Column(db.String(30), default='student')


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    password = db.Column(db.String(30))
    role = db.Column(db.String(30), default='teacher')

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    designation = db.Column(db.String(30))
    dept = db.Column(db.String(30))
    role = db.Column(db.String(30), default = 'admin')

    
class Assignments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    branch = db.Column(db.String(4),db.ForeignKey('branch.branch'))
    subject = db.Column(db.String(30))
    semester = db.Column(db.Integer)
    assignment = db.Column(db.String(30))
    max_marks = db.Column(db.Integer)
    
class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    assignment = db.Column(db.String(30))
    marks = db.Column(db.Integer, default = 0)
    rollno = db.Column(db.String(30), db.ForeignKey('student.rollno'))
    lab = db.Column(db.Integer, default = 0)
    
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(4),db.ForeignKey('branch.branch'))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    teacher_id = db.Column(db.String(30), db.ForeignKey('teacher.id'))
    subject = db.Column(db.String(30))
    
class Complaints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    complaint = db.Column(db.String(200))
    dept = db.Column(db.String(30), db.ForeignKey('admin.dept'))
    
class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(4), db.ForeignKey('branch.branch'))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    Mon1 = db.Column(db.Integer)
    Mon2 = db.Column(db.Integer)
    Mon3= db.Column(db.Integer)
    Mon4 = db.Column(db.Integer)
    Mon5 = db.Column(db.Integer)
    Tue1 = db.Column(db.Integer)
    Tue2 = db.Column(db.Integer)
    Tue3= db.Column(db.Integer)
    Tue4 = db.Column(db.Integer)
    Tue5 = db.Column(db.Integer)
    Wed1 = db.Column(db.Integer)
    Wed2 = db.Column(db.Integer)
    Wed3= db.Column(db.Integer)
    Wed4 = db.Column(db.Integer)
    Wed5 = db.Column(db.Integer)
    Thu1 = db.Column(db.Integer)
    Thu2 = db.Column(db.Integer)
    Thu3= db.Column(db.Integer)
    Thu4 = db.Column(db.Integer)
    Thu5 = db.Column(db.Integer)
    Fri1 = db.Column(db.Integer)
    Fri2 = db.Column(db.Integer)
    Fri3= db.Column(db.Integer)
    Fri4 = db.Column(db.Integer)
    Fri5 = db.Column(db.Integer)
    
class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(4), db.ForeignKey('branch.branch'))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    A1 = db.Column(db.Integer)
    A = db.Column(db.Integer)
    B = db.Column(db.Integer)
    C = db.Column(db.Integer)
    F = db.Column(db.Integer)
    
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(30))
    content = db.Column(db.String(300))