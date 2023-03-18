from flask_restx import Namespace, Resource, fields
from flask import request, json, abort
from ..models.student import Student
from ..models.admin import Admin
from ..utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import string
import random
from functools import wraps

def admin_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            abort(403, 'You must be an admin to access this resource')
        return func(*args, **kwargs)
    return decorated

student_namespace = Namespace('student', description='Namespace for Student Operations')

student_model = student_namespace.model(
    'CreateStudent', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A Username"),
        'email': fields.String(required=True, description="An Email"),
        'password': fields.String(required=True, description="A Password"),
        'student_id': fields.String(required=True, description="A Student Id"),
        'grade': fields.Integer(decscription="Student Grade"),
        'gpa': fields.Float(description="Stuent GPA")
    }
)

studentt_model = student_namespace.model(
    'CreateStudent', {
        'username': fields.String(required=True, description="A Username"),
        'email': fields.String(required=True, description="An Email")
    }
)
edit_student_model = student_namespace.model(
    'EditStudent', {
        'grade': fields.Integer(required=True, description="Student Grade"),
        'gpa': fields.Float(required=True, description="Student GPA")
    }
)

loginn_model = student_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An Email"),
        'password': fields.String(required=True, description="A Password")
    }
)

@student_namespace.route('/login')
class Login(Resource):
    @student_namespace.expect(loginn_model)
    def post(self):
        """
           Generate JWT Token

        """
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        student = Student.query.filter_by(email=email).first()

        if (student is not None) and (student.password==password):
            access_token = create_access_token(identity=student.username)
            refresh_token = create_refresh_token(identity=student.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED

@student_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """

            Generate Refresh Token

        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK
    

@student_namespace.route('/students')
class OrderGetCreate(Resource):
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Get All Students'
    )
    @jwt_required()
    @admin_required
    def get(self):
        """

           Get All Students

        """
        student = Student.query.all()

        return student, HTTPStatus.OK
    
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description='Create A Student'
    )
    @jwt_required()
    @admin_required
    def post(self):
        """
           Create A Student

        """

        data = student_namespace.payload

        new_student = Student(
            username = data['username'],
            email = data['email'],
            password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8)),
            student_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        )

        new_student.save()

        return new_student, HTTPStatus.CREATED

@student_namespace.route('/student/<int:student_id>')
class GetUpdateDelete(Resource):
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = 'Retrieve A Student By ID',
        params = {'Course_id': 'An ID For A Student'}
    )
    @jwt_required()
    def get(self, student_id):
        """

           Retrieving a Student by id

        """
        student = Student.get_by_id(student_id)

        return student, HTTPStatus.OK

    @student_namespace.doc(
        description = 'Update A Student Password By ID',
        params = {'order_id': 'An ID For A Student'}
    )
    @jwt_required()
    def put(self, student_id):
        """

           Student Please Update Your Password

        """
        student_to_update = Student.get_by_id(student_id)

        data = student_namespace.payload

        student_to_update.password = data["password"]

        db.session.commit()

        return student_to_update, HTTPStatus.OK
    
    @student_namespace.expect(edit_student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description = 'Update A Student Records By ID',
        params = {'order_id': 'An ID For A Student'}
    )
    @jwt_required()
    def put(self, student_id):
        """

           Upddate Student Records

        """
        student_to_update = Student.get_by_id(student_id)

        data = student_namespace.payload

        student_to_update.grade = data["grade"]
        student_to_update.gpa = data["gpa"]

        db.session.commit()

        return student_to_update, HTTPStatus.OK
    
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
            description = 'Delete Student',
            params = {'order_id': 'An ID For A Student'}
    )
    @jwt_required()
    def delete(self, student_id):
        """

           Delete a Student by Id

        """
        student_to_delete = Student.get_by_id(student_id)
        student_to_delete.delete()

        return {"message": "Student Deleted Successfully!"}, HTTPStatus.OK


@student_namespace.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """
           
           Logout Student

        """
        unset_jwt_cookies
        db.session.commit()
        return {"Message": "Logged out already!"}, HTTPStatus.OK