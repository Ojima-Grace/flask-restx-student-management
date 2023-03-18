from flask import Flask
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.admin import Admin
from .models.student import Student
from .models.course import Course
from .models.enrollment import Enrollment
from .auth.views import auth_namespace
from .course.views import course_namespace
from .student.views import student_namespace
from .enrollment.views import enrollment_namespace
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT token to the header with Bearer &lt;JWT&gt; token to authorize **"
        }
    }
    api = Api(app,
              title='STUDENT MANAGEMENT API',
              description="A Student Management Api Built With Flask RestX",
              authorizations=authorizations,
              security='Bearer Auth'
              )
    
    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(student_namespace, path='/student')
    api.add_namespace(course_namespace, path='/course')
    api.add_namespace(enrollment_namespace, path='/enrollment')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Message Not Allowed"}, 404
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'student': Student,
            'course': Course,
            'admin': Admin,
            'enrollments': Enrollment  
        }
    
    return app