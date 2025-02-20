from flask import Flask
from flask_cors import CORS
from models import *
from config import DevelopmentConfig
import os
from flask_jwt_extended import JWTManager
from flask_restful import Api

from auth import login,create, updateRole, usernameInfo, getRole, addRequest, learnerCourses
from admin import adminCourse, requestPage, updateTutor
from learner import allMyCourses
from tutor import tutorCourse, topicRequest, courseTopics, topicContent, addVideoLink, add_quiz_question,add_coding_quiz


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    return app
app = create_app()
CORS(app)

app.app_context().push()
jwt = JWTManager(app)

api = Api(app)
api.add_resource(login,'/api/login')
api.add_resource(create,'/api/create')
api.add_resource(updateRole,'/api/update/role')
api.add_resource(getRole,'/api/get-role')
api.add_resource(adminCourse,'/api//admin/courses')
api.add_resource(usernameInfo,'/api/info/username')
api.add_resource(addRequest, '/api/tutor/add-request')
api.add_resource(requestPage,'/api/admin/requests')
api.add_resource(updateTutor, '/api/update/course-tutor')
api.add_resource(learnerCourses, '/api/learner/add-course')
api.add_resource(allMyCourses, '/api/learner/my-courses')
api.add_resource(tutorCourse, '/api/tutor/course')
api.add_resource(topicRequest,'/api/tutor/add_topic')
api.add_resource(courseTopics,'/api/tutor/course/get-topics','/api/learner/course/get-topics')
api.add_resource(topicContent,'/api/tutor/topic/content','/api/learner/topic/content')
api.add_resource(addVideoLink,'/api/tutor/add_video')
api.add_resource(add_quiz_question,'/api/tutor/add_quiz_question')
api.add_resource(add_coding_quiz,'/api/tutor/add_coding_quiz')
# Ensure the directory exists
if not os.path.exists('instance'):
    os.makedirs('instance')

file_path = os.path.join(os.getcwd(), 'instance', 'database.sqlite3')
if not os.path.exists(file_path):
    with app.app_context():
        db.create_all()
        try:
            admin_user = User(username='Admin', password='1234', role=3)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user added successfully")
        except Exception as e:
            db.session.rollback()  # Rollback changes if an error occurs
            print(f"Error adding admin user: {str(e)}")
        finally:
            print("print something")

if __name__=="__main__":
    app.run()