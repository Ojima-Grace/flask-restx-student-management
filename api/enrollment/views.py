from flask_restx import Namespace, Resource, fields
from ..models.course import Course
from ..models.student import Student
from ..models.enrollment import Enrollment
from ..utils import db
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import string
import random



enrollment_namespace = Namespace('enrollments', description='Name Space For Enrollments')

enrollment_model = enrollment_namespace.model(
    'Enrollment', {
        'id': fields.Integer(description='An ID'),
        'course_id': fields.Integer(description='Course ID'),
        'student_id': fields.Integer(description='Student ID')
    }
)

@enrollment_namespace.route('/enrollments')
class OrderGetCreate(Resource):
    @enrollment_namespace.marshal_with(enrollment_model)
    @enrollment_namespace.doc(
        description='Get All Courses'
    )
    @jwt_required()
    def get(self):
        """

           Get All Course

        """
        enrollment = Enrollment.query.all()

        return enrollment, HTTPStatus.OK
    
@enrollment_namespace.route('/course/<int:course_id>/student/<int:student_id>')
class EnrollmentResource(Resource):
    #@enrollment_namespace.marshal_with(enrollment_model)
    @enrollment_namespace.doc(
            description = 'Student Enroll',
            params = {'Course_ID': 'An ID For A Course',
                      'Student_ID': 'An ID For A Student'
                     }
    )
    @jwt_required()
    def post(self, course_id, student_id):
        """
        Enroll a student in a course
        """
        course = Course.get_by_id(course_id)
        student = Student.get_by_id(student_id)
        
        student_in_course =  Enrollment.query.filter_by(
                student_id=student.id, course_id=course.id
            ).first()
        if student_in_course:
            return {
                "message": f"{student.student_id} is already registered for {course.id}"
            }, HTTPStatus.OK
        
        course_student =  Enrollment(
            course_id = course_id,
            student_id = student_id
        )

        course_student.save()

        return {"message": "Congratulations! You are now enrolled"}, HTTPStatus.CREATED.value

@enrollment_namespace.route('/course/<int:course_id>/students')
class GetAllCourseStudents(Resource):
    #@enrollment_namespace.expect(enrollment_model)
    @enrollment_namespace.marshal_with(enrollment_model)
    @enrollment_namespace.doc(
        description='List all students registered in a course',
        params = {'Course_ID': 'An ID For A Course'
                 }
    )
    @jwt_required()
    def get(self, course_id):
        """
        List all students registered in a course
        """
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()

        return enrollments, HTTPStatus.OK
    