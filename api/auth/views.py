from flask_restx import Namespace, Resource, fields
from flask import request, json
from ..models.admin import Admin
from ..utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import string
import random


auth_namespace = Namespace('auth', description='Namespace for Authentication')

signup_model = auth_namespace.model(
    'Signup', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A Username"),
        'email': fields.String(required=True, description="An Email"),
        'password': fields.String(required=True, description="A Password")
    }
)

admin_model = auth_namespace.model(
    'Admin', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description="A Username"),
        'email': fields.String(required=True, description="An Email"),
        'password_hash': fields.String(required=True, description="A Password"),
        'is_admin': fields.Boolean(description="This shows whether user is active or not")
        }
)

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description="An Email"),
        'password': fields.String(required=True, description="A Password")
    }
)

@auth_namespace.route('/admins')
class OrderGetCreate(Resource):
    #@student_namespace.expect(student_model)
    @auth_namespace.marshal_with(admin_model)
    @auth_namespace.doc(
        description='Get All Admins'
    )
    @jwt_required()
    def get(self):
        """

           Get All Admins

        """
        admins = Admin.query.all()

        return admins, HTTPStatus.OK
    
@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(admin_model)
    def post(self):
        """
           Signup A User

        """
        data = request.get_json()

        new_admin = Admin(
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )
        new_admin.save()

        return new_admin, HTTPStatus.CREATED

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
           Generate JWT Token

        """
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        admin = Admin.query.filter_by(email=email).first()

        if (admin is not None) and check_password_hash(admin.password_hash,password):
            access_token = create_access_token(identity=admin.username)
            refresh_token = create_refresh_token(identity=admin.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED

@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """

            Generate Refresh Token

        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {'access_token': access_token}, HTTPStatus.OK
    
@auth_namespace.route('/admin/<int:admin_id>')
class GetUpdateDelete(Resource):
    @auth_namespace.marshal_with(admin_model)
    @auth_namespace.doc(
        description = 'Retrieve An Admin By ID',
        params = {'Admin_ID': 'An ID For A Admin'}
    )
    @jwt_required()
    def get(self, admin_id):
        """

           Retrieving An Admin by Id

        """
        admin = Admin.get_by_id(admin_id)

        return admin, HTTPStatus.OK
    
    
    # @auth_namespace.expect(edit_admin_model)
    # @auth_namespace.marshal_with(admin_model)
    # @auth_namespace.doc(
    #     description = 'Update An Admin By ID',
    #     params = {'Admin_ID': 'An ID For An Admin'}
    # )
    # @jwt_required()
    # def put(self, admin_id):
    #     """

    #        Upddate Admin

    #     """
    #     admin_update = Admin.get_by_id(admin_id)

    #     data = auth_namespace.payload

    #     admin_update.username = data["username"]
    #     student_update.password = data["password"]

    #     db.session.commit()

    #     return admin_update, HTTPStatus.OK
    
    @auth_namespace.expect(admin_model)
    @auth_namespace.marshal_with(admin_model)
    @auth_namespace.doc(
            description = 'Delete Admin',
            params = {'Admin_ID': 'An ID For An Admin'}
    )
    @jwt_required()
    def delete(self, admin_id):
        """

           Delete An Admin by Id

        """
        admin_to_delete = Admin.get_by_id(admin_id)
        admin_to_delete.delete()

        return {"message": "Admin Deleted Successfully!"}, HTTPStatus.OK

@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """
           
           Logout Admin

        """
        unset_jwt_cookies
        db.session.commit()
        return {"Message": "Logged out successfully!"}, HTTPStatus.OK