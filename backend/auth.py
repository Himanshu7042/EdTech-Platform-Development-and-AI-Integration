from flask import session, request
from flask_restful import Resource,reqparse
from models import *
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime 

class login(Resource):
    def post(self):
        loginparser = reqparse.RequestParser()
        loginparser.add_argument('username', type=str)
        loginparser.add_argument('password', type=str)
        args = loginparser.parse_args()

        if args['username'] and args['password']:
            user = User.query.filter_by(username=args['username'],password=args['password']).first()
            if user :
                access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(minutes=240) )
                return {"username":user.username ,"role":user.role,"access_token":access_token}, 200
            else :
                return {'message' : 'user not found '}, 404

class create(Resource):
    def post(self):
        from sqlalchemy.exc import IntegrityError

        try:
            signUpParser = reqparse.RequestParser()
            signUpParser.add_argument('username', type=str)
            signUpParser.add_argument('password', type=str)
            args = signUpParser.parse_args()
            user = User(username=args['username'],password=args['password'],role=0)
            db.session.add(user)
            access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(minutes=240) )
            return {"access_token":access_token,'message': 'signup successful'}, 200
        except:
            db.session.rollback()
            return {'message':'username already exists'}, 400
        finally:
            db.session.commit()


class updateRole(Resource):
    @jwt_required()
    def __init__(self) :
        self.username = get_jwt_identity()
    @jwt_required()
    def put(self):
        roleparser = reqparse.RequestParser()
        roleparser.add_argument('role')
        roleparser.add_argument('username')
        args = roleparser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        user.role = args['role'] 
        db.session.commit()
        return {"message": "Role updated successfully"}, 200
    
class usernameInfo(Resource):
    @jwt_required()
    def get(self):
        # Get the username from the JWT payload
        username = get_jwt_identity()
        # Return the username along with the HTTP status code
        return {"username": username}, 200
    

class getRole(Resource):
    @jwt_required()
    def post(self):
        roleParser = reqparse.RequestParser()
        roleParser.add_argument('username', type=str)
        args = roleParser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user:
            return {'role': user.role}, 200

class addRequest(Resource):
    def post(self):
        try:
            Parser = reqparse.RequestParser()
            Parser.add_argument('username', type=str)
            Parser.add_argument('courseId', type=str)
            args = Parser.parse_args()
            request = TutorRequest(username=args['username'],courseId=args['courseId'])
            db.session.add(request)
            return {'message':'Tutor request added successfully'}, 200
        except:
            db.session.rollback()
            return {'message':'something went wrong in adding request for tutor'}, 400
        finally:
            db.session.commit()


class learnerCourses(Resource):
    @jwt_required()
    def post(self):
        try:
            Parser = reqparse.RequestParser()
            Parser.add_argument('username', type=str, required=True)
            Parser.add_argument('courseId', type=str, required=True)
            args = Parser.parse_args()
            print(args)
            l_course = MyCourses(username=args['username'], courseId=args['courseId'])
            db.session.add(l_course)
            return {'message': 'learner course added successfully'}, 200
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  # Print the error for debugging
            return {'message': 'Something went wrong in adding learner courses'}, 400
        finally:
            db.session.commit()

