from ..utils import db
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer(), primary_key=True)
    course_name = db.Column(db.String(), default="PYTHON")
    teacher = db.Column(db.String(), default="CALEB EMELIKE")
    enrollment = db.relationship('Enrollment', backref='course', lazy=True)


    def __repr__(self):
        return f"<Course {self.id}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_by_id(cls, id):
        return  cls.query.get_or_404(id)