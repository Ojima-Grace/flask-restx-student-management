import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.student import Student
from flask_jwt_extended import create_access_token
import random
import string

class StudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()
        self.app = None
        self.client = None
    
    def test_get_all_students(self):
        token = create_access_token(identity='testuser')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get('/student/studentss', headers=headers)

        assert response.status_code == 200
        assert response.json == []

    def test_create_a_student(self):
        data = {
            "username": "teststudent",
            "email": "test@student.com",
            "password": "kiki",
            "student_id": "A2023"
        }
        token = create_access_token(identity="testuser")
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.post('/student/students', json=data, headers=headers)
        assert response.status_code == 201
        student = Student.query.all()
        student_id = student[0].id
        assert student_id == 1
        assert len(student) == 1

    def test_student_login(self):
        data = {
            "email": "test@test.com.com",
            "password": "password"
        }

        response = self.client.post('student/login', json=data)

        assert response.status_code == 200