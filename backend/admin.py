from flask import session, request, abort, jsonify
from flask_restful import Resource,reqparse
from sqlalchemy import distinct
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

class adminCourse(Resource):
    
    
    def post(self):
        
        sectionparser = reqparse.RequestParser()
        sectionparser.add_argument('courseId')
        sectionparser.add_argument('courseName')
        sectionparser.add_argument('courseTutorId')

        args = sectionparser.parse_args()


        # # Check if courseId is already in the database
        existing_book = Course.query.filter_by(courseId=args["courseId"]).first()
        if existing_book:
            abort(409, description="courseId is already in the database")

        course = Course(courseId=args["courseId"], courseName=args["courseName"])
        db.session.add(course)
        db.session.commit()
        return "Course added successfully"
    
    def get(self):
        courses = Course.query.all()
        courses = [{'courseId':course.courseId, 'courseName':course.courseName,'courseTutorId':course.courseTutorId}
                   for course in courses]
        return courses

class requestPage(Resource):
    @jwt_required()
    def get(self):
        role = request.args.get('role', None)
        
        combined_data = db.session.query(TutorRequest, User, Course).join(
            User, TutorRequest.username == User.username).join(
            Course, TutorRequest.courseId == Course.courseId
        ).filter(User.role == role).all()

        result = []
        if combined_data != []:
            for tutor_request,user, course in combined_data:
                result.append({
                    'username': tutor_request.username,
                    'courseId': tutor_request.courseId,
                    'course_name': course.courseName,
                })
        return result, 200
    
class updateTutor(Resource):
    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('courseId')
        parser.add_argument('username')
        args = parser.parse_args()
        course = Course.query.filter_by(courseId=args['courseId']).first()
        course.courseTutorId = args['username'] 
        db.session.commit()
        return {"message": "Course Tutor updated successfully"}, 200