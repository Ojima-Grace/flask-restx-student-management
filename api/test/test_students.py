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


    def test_student_login(self):
        data = {
            "email": "test@test.com.com",
            "password": "password"
        }

        response = self.client.post('auth/login', json=data)

        assert response.status_code == 200