import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..utils import db
from flask_jwt_extended import create_access_token
from ..models.course import Course

class UserTestCase(unittest.TestCase):
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

    def test_get_all_courses(self):
        token = create_access_token(identity='ojima')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.get('/course/courses', headers=headers)

        assert response.status_code == 200
        assert response.json == []

    def test_create_course(self):
        data = {
            "course_name": "Python",
            "teacher": "test"
        }

        token = create_access_token(identity="ojima")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = self.client.post('/course/courses', json=data, headers=headers)
        assert response.status_code == 201
        course = Course.query.all()
        course_id = course[0].id
        assert course_id == 1
        assert len(course) == 1

    def test_get_single_course(self):
        course = Course(
            course_name = "Python",
            teacher = "test"
        )
        course.save()
        token = create_access_token(identity='ojima')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response= self.client.get('/course/courses/1', headers=headers)
        assert response.status_code == 404

    def test_delete_course_by_id(self):
        course = Course(
            course_name = "Python",
            teacher = "test"
        )
        course.save()
        token = create_access_token(identity='ojima')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response= self.client.delete('/course/courses/1', headers=headers)
        assert response.status_code == 404
