import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.enrollment import Enrollment
from ..models.course import Course
from ..models.student import Student
from flask_jwt_extended import create_access_token

class EnrollmentTestCase(unittest.TestCase):
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

    def test_get_all_enrollments(self):
        token = create_access_token(identity='testuser')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get('/enrollment/enrollmentss', headers=headers)
        assert response.status_code == 200
        assert response.json == []

    def test_enrollment(self):
        response = self.client.post('/course/1/2')

        assert response.status_code == 404

