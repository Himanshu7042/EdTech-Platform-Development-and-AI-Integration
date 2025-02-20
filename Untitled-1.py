@app.route('/api/tutor/course', methods=['GET'])
def get_courses():
    username = request.args.get('username')
    my_courses = MyCourses.query.filter_by(username=username).all()
    courses = [Course.query.get(course.courseId) for course in my_courses]
    return jsonify([{"courseId": course.courseId, "courseName": course.courseName} for course in courses])

@app.route('/api/tutor/topics', methods=['GET'])
def get_topics():
    course_id = request.args.get('courseId')
    topics = Topic.query.filter_by(courseId=course_id).all()
    return jsonify([{"id": topic.id, "name": topic.name, "content": {
        "video": Video.query.filter_by(topicId=topic.id).first(),
        "quiz": Quiz.query.filter_by(topicId=topic.id).first(),
        "codingQuiz": CodingQuiz.query.filter_by(topicId=topic.id).first(),
    }} for topic in topics])

@app.route('/api/tutor/add_topic', methods=['POST'])
def add_topic():
    data = request.json
    new_topic = Topic(name=data['name'], courseId=data['courseId'])
    db.session.add(new_topic)
    db.session.commit()
    return jsonify({"id": new_topic.id, "name": new_topic.name})

@app.route('/api/tutor/add_video', methods=['POST'])
def add_video():
    data = request.json
    new_video = Video(link=data['link'], topicId=data['topicId'])
    db.session.add(new_video)
    db.session.commit()
    return jsonify({"id": new_video.id, "link": new_video.link})

@app.route('/api/tutor/add_quiz_question', methods=['POST'])
def add_quiz_question():
    data = request.json
    new_question = QuizQuestion(question=data['question'], options=data['options'], correct_option=data['correct_option'], quizId=data['quizId'])
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"id": new_question.id, "question": new_question.question})

@app.route('/api/tutor/add_coding_quiz', methods=['POST'])
def add_coding_quiz():
    data = request.json
    new_coding_quiz = CodingQuiz(question=data['question'], test_cases=data['test_cases'], topicId=data['topicId'])
    db.session.add(new_coding_quiz)
    db.session.commit()
    return jsonify({"id": new_coding_quiz.id, "question": new_coding_quiz.question})