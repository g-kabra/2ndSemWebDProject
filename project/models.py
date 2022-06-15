from . import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    # rollno = db.Column(db.String(30))
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    branch = db.Column(db.String(4))
    year = db.Column(db.Integer)
    password = db.Column(db.String(30))