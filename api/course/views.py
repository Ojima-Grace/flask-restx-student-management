from flask_restx import Namespace, Resource, fields
from ..models.course import Course
from ..models.student import Student
from ..utils import db
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import string
import random

course_namespace = Namespace('courses', description='Name Space For Course')

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(description='An ID'),
        'course_name': fields.String(description='COURSE NAME'),
        'teacher': fields.String(description='NAME OF TEACHER')
    }
)

@course_namespace.route('/courses')
class OrderGetCreate(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get All Courses'
    )
    @jwt_required()
    def get(self):
        """

           Get All Course

        """
        course = Course.query.all()

        return course, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Create A Course'
    )
    @jwt_required()
    def post(self):
        """
           Create A Course
        """
        data = course_namespace.payload

        new_course = Course(
            course_name = data['course_name'],
            teacher = data['teacher']
        )

        new_course.save()

        return new_course, HTTPStatus.CREATED
        
@course_namespace.route('/course/<int:course_id>')
class GetUpdateDelete(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = 'Retrieve A Course By ID',
        params = {'Course_id': 'An ID For A Course'}
    )
    @jwt_required()
    def get(self, course_id):
        """

           Retrieving a course by id

        """
        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description = 'Update A Course By ID',
        params = {'order_id': 'An ID For A Course'}
    )
    @jwt_required()
    def put(self, course_id):
        """

           Update a course by id

        """
        course_to_update = Course.get_by_id(course_id)

        data = course_namespace.payload

        course_to_update.course_name = data["course_name"]
        course_to_update.teacher = data["teacher"]

        db.session.commit()

        return course_to_update, HTTPStatus.OK
    
    @course_namespace.doc(
            description = 'Delete A Course By ID',
            params = {'order_id': 'An ID For A Course'}
    )
    @jwt_required()
    def delete(self, course_id):
        """

           Delete a course by id

        """
        course_to_delete = Course.get_by_id(course_id)
        course_to_delete.delete()

        return {"message": "Course Deleted Successfully!"}, HTTPStatus.OK