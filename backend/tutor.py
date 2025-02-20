from flask import session, request, abort, jsonify
from flask_restful import Resource,reqparse
from sqlalchemy import distinct
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity

class tutorCourse(Resource):
    @jwt_required()
    def get(self):
        username = request.args.get('username', None)
        # Handle missing username parameter
        if not username:
            return {"message": "Username parameter is missing."}, 400
        combined_data = db.session.query(Course).filter(
            Course.courseTutorId == username).all()
        
        result = []
        if combined_data != []:
            for course in combined_data:
                result.append({
                    'courseId': course.courseId,
                    'courseName': course.courseName,
                })
        return result, 200

        
class topicRequest(Resource):
    @jwt_required()
    def post(self):
        try:
            parse = reqparse.RequestParser()
            parse.add_argument('courseId', type=str, required=True, help='Course ID must be a string')
            parse.add_argument('newTopicName', type=str, required=True, help='Topic name cannot be blank')
            parse.add_argument('includeQuiz', type=bool, required=True, help='Include Quiz must be a boolean')
            parse.add_argument('includeCodingQuiz', type=bool, required=True, help='Include Coding Quiz must be a boolean')
            parse.add_argument('includeVideo', type=bool, required=True, help='Include Video must be a boolean')
            args = parse.parse_args()

            # Create and save the new topic
            new_topic = Topic(name=args['newTopicName'], courseId=args['courseId'])
            db.session.add(new_topic)
            db.session.commit()
            
            topic_id = new_topic.id

            # Process the included content types
            if args['includeVideo']:
                self.create_videoId(topic_id)
            if args['includeQuiz']:
                self.create_QuizId(topic_id)
            if args['includeCodingQuiz']:
                self.create_CodingQuizId(topic_id)

            return {"message": "Topic added successfully"}, 200
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Error occurred in adding topic", "error": str(e)}, 400

    def create_videoId(self, topic_id):
        new_video = Video(topicId=topic_id)
        db.session.add(new_video)
        db.session.commit()
        
    def create_QuizId(self, topic_id):
        new_quiz = Quiz(topicId=topic_id)
        db.session.add(new_quiz)
        db.session.commit()
        
    def create_CodingQuizId(self, topic_id):
        new_coding_quiz = CodingQuiz(topicId=topic_id)
        db.session.add(new_coding_quiz)
        db.session.commit()


class courseTopics(Resource):
    @jwt_required()
    def get(self):
        courseId = request.args.get('courseId', None)

        if not courseId:
            return {"message": "CourseId parameter is missing."}, 400
        
        combined_topics = Topic.query.filter_by(courseId=courseId).all()
        
        result = []
        if combined_topics != []:
            for data in combined_topics:
                result.append({
                    'id': data.id,
                    'name': data.name,
                    'content': {
                        'video': self.have_video(data.id),
                        'quiz': self.have_quiz(data.id),
                        'codingQuiz': self.have_codingQuiz(data.id)
                    }
                })
        return result, 200


    def have_video(self,topicId):
        q = Video.query.filter_by(topicId = topicId).first()
        if q:
            return True
        return False
    
    def have_quiz(self,topicId):
        q = Quiz.query.filter_by(topicId = topicId).first()
        if q:
            return True
        return False
    
    def have_codingQuiz(self,topicId):
        q = CodingQuiz.query.filter_by(topicId = topicId).first()
        if q:
            return True
        return False
    
# "content": [
#                         {"type": "video", "details": "url_or_other_info"},
#                         {"type": "codingQuiz", "details": "quiz_data"}
#                     ]

class topicContent(Resource):
    jwt_required()
    def get(self):
        topicId = request.args.get('topicId', None)
        type = request.args.get('type', None)

        if not topicId and not type:
            return {"message": "CourseId parameter is missing."}, 400
        
        if type=='video':
            output = Video.query.filter_by(topicId=topicId).first()
            return {'type':'video','details': {'id': output.id, 'link' : output.link} }

        elif type=='quiz':
            first_output = Quiz.query.filter_by(topicId=topicId).first()
            mid_out = QuizQuestion.query.filter_by(quizId=first_output.id).all()
            if mid_out:
                output = []
                for question in mid_out:
                    x = {'id':question.id,
                        'question':question.question,
                        'options':question.options,
                        'correct_option':question.correct_option}
                    output.append(x)
                
                return {'type':'quiz', 'quizId':question.quizId, 'details': output},200
            else:
                output = []
                x = {'id': None,
                        'question':None,
                        'options':None,
                        'correct_option':None}
                output.append(x)
                
                return {'type':'quiz','quizId':first_output.id, 'details': output},200

        elif type=='codingQuiz':
            output = CodingQuiz.query.filter_by(topicId=topicId).first()
            return {'type':'codingQuiz','details': {'id': output.id,'language':output.language ,'question' : output.question, 'test_cases':output.test_cases} },200
        
        else:
            return {'message': 'Something went wrong'}, 400

class addVideoLink(Resource):
    jwt_required()
    def put(self):
        parse = reqparse.RequestParser()
        parse.add_argument('videoId')
        parse.add_argument('videoLink')
        args = parse.parse_args()
        video = Video.query.filter_by(id=args['videoId']).first()
        video.link = args['videoLink']
        db.session.commit()
        
        return {'message':'Video link updated'}


class add_quiz_question(Resource):
    def post(self):
        data = request.json
        new_question = QuizQuestion(question=data['question'], options=data['options'], correct_option=data['correctOption'], quizId=data['quizId'])
        db.session.add(new_question)
        db.session.commit()
        print("Question added")
      
class add_coding_quiz(Resource): 
    def put(self):
        data = request.json
        print(data['id'])
        question = CodingQuiz.query.filter_by(id=data['id']).first()
        question.language = data['language']
        question.question = data['question']
        question.test_cases = data['testCases']
        db.session.commit()
        
        return {'message':'Programming question updated'}
      
