from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    role = db.Column(db.Integer, default=0)  # 0 for students, 1 for tutors, 2 for admins

class Course(db.Model):
    courseId = db.Column(db.String(10), primary_key=True)
    courseName = db.Column(db.String(30), nullable=False)
    courseTutorId = db.Column(db.String(50), db.ForeignKey('user.username'))

class TutorRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), db.ForeignKey('user.username'))
    courseId = db.Column(db.String(50), db.ForeignKey('course.courseId'))

class MyCourses(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), db.ForeignKey('user.username'))
    courseId = db.Column(db.String(50), db.ForeignKey('course.courseId'))

#

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    courseId = db.Column(db.String(50), db.ForeignKey('course.courseId'))

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(200))
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(500), nullable=False)
    options = db.Column(db.JSON, nullable=False)  # A JSON field to store multiple choice options
    correct_option = db.Column(db.String(100), nullable=False)
    quizId = db.Column(db.Integer, db.ForeignKey('quiz.id'))

class CodingQuiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language = db.Column(db.String(20))
    question = db.Column(db.String(1000))
    test_cases = db.Column(db.JSON)  # A JSON field to store test cases
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))

