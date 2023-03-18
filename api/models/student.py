from ..utils import db
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship



class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    student_id = db.Column(db.String(), nullable=False)
    grade = db.Column(db.Integer(), default=0)
    gpa = db.Column(db.Float(), default=0.0)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    enrollment = db.relationship('Enrollment', backref='user', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return  cls.query.get_or_404(id)