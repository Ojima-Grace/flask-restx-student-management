from ..utils import db
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))

    def __init__(self, course_id, student_id):
        self.course_id = course_id
        self.student_id = student_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return  cls.query.get_or_404(id)


    @classmethod
    def get_by_id(cls, id):
        return  cls.query.get_or_404(id)