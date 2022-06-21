from . import db
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    rollno = db.Column(db.String(30))
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    branch = db.Column(db.String(4))
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
    branch = db.Column(db.String(4))
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
    
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(4))
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
    branch = db.Column(db.String(4))
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    Mon1 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Mon2 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Mon3= db.Column(db.Integer, db.ForeignKey('subject.id'))
    Mon4 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Mon5 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Tue1 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Tue2 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Tue3= db.Column(db.Integer, db.ForeignKey('subject.id'))
    Tue4 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Tue5 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Wed1 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Wed2 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Wed3= db.Column(db.Integer, db.ForeignKey('subject.id'))
    Wed4 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Wed5 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Thu1 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Thu2 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Thu3= db.Column(db.Integer, db.ForeignKey('subject.id'))
    Thu4 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Thu5 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Fri1 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Fri2 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Fri3= db.Column(db.Integer, db.ForeignKey('subject.id'))
    Fri4 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    Fri5 = db.Column(db.Integer, db.ForeignKey('subject.id'))
    
    
    
    
