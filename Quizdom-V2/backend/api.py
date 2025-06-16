# Import Flask-RESTful's Resource base class for creating API resources
from flask_restful import Resource
# Import Flask's request object for accessing incoming request data
from flask import request
# Import JWT decorators and helpers for authentication and identity management
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt, verify_jwt_in_request
# Import database models (ORM classes) for all entities
from backend.models import db, User, Subject, Chapter, Quiz, Question, Score
# Import datetime for date/time handling
from datetime import datetime
# Import bcrypt for secure password hashing and verification
from passlib.hash import bcrypt
# Import Celery tasks (for background jobs like exporting scores)
from backend.task import*

# -------------------------------------------------------------------
# User Login Resource: Handles user authentication and JWT issuance
# -------------------------------------------------------------------
class User_Login(Resource):
    def post(self):
        # Get JSON data from the request body
        data = request.get_json()
        # Find user in the database by username
        user = User.query.filter_by(user_name = data['user_name']).first()
        # If user not found, return an error
        if not user:
            return {'message': 'User does not exist'}, 401
        # If user exists, verify the password using bcrypt
        if user and bcrypt.verify(data['user_password'], user.user_password):
            # Create a JWT access token with the username and user_id as claims
            access_token = create_access_token(identity = user.user_name,
                                               additional_claims = {"user_id": user.user_id})
            # If user is an admin, return admin login message and token
            if user.user_is_administrator:
                return {'message': 'Admin logged in successfully',
                        'access_token': access_token,
                        'user_id': user.user_id,
                        'user_name': user.user_name}, 200
            else:
                # If regular user, return user login message and token
                return {'message': 'User logged in successfully',
                        'access_token': access_token,
                        'user_id': user.user_id,
                        'user_name': user.user_name}, 200
        else:
            # If password is incorrect, return error
            return {'message': 'Invalid username or password'}, 401    

# -------------------------------------------------------------------
# User Signup Resource: Handles new user registration
# -------------------------------------------------------------------
class User_Signup(Resource):
    def post(self):      
        # Get JSON data from the request body
        data = request.get_json()
        # Check if a user with the same username already exists
        user = User.query.filter_by(user_name = data['user_name']).first()
        if user:
            return {'message': 'User already exists'}, 400
        # Create a new User object with hashed password and other details
        user = User(user_name = data['user_name'],
                    user_email = data['user_email'],
                    user_password = bcrypt.hash(data['user_password']),
                    user_dob = datetime.strptime(data['user_dob'], '%Y-%m-%d').date(),
                    user_complete_name = data['user_complete_name'],
                    user_education_level = data['user_education_level'])
        # Add the new user to the database
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 200

# -------------------------------------------------------------------
# Subject Management Resource (Admin Only): CRUD for subjects
# -------------------------------------------------------------------
class Add_Subject(Resource):
    @jwt_required()
    def get(self):
        # Get the current user's identity from the JWT token
        current_user = get_jwt_identity()
        # Only admin can access this endpoint
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        # Fetch all subjects from the database
        subjects = Subject.query.all()
        subject_json = []
        # For each subject, also fetch and include its chapters
        for subject in subjects:
            chapters = Chapter.query.filter_by(subject_id_of_chapter = subject.subject_id).all()
            chapter_json = []
            for chapter in chapters:
                chapter_json.append({
                    "chapter_id": chapter.chapter_id,
                    "chapter_name": chapter.chapter_name,
                    "chapter_description": chapter.chapter_description
                    })
            subject_json.append({
                "subject_id": subject.subject_id,
                "subject_name": subject.subject_name,
                "subject_description": subject.subject_description,
                "chapters": chapter_json
                })
        # Return the list of subjects (with chapters) as JSON
        return subject_json, 200    

    @jwt_required()
    def post(self):
        # Only admin can add a new subject
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        # Get subject data from request
        data = request.get_json()
        # Create and add the new subject to the database
        subject = Subject(subject_name = data['subject_name'], subject_description = data['subject_description'])
        db.session.add(subject)
        db.session.commit()
        return {'message': 'Subject added successfully'}, 200  

    @jwt_required()
    def put(self, sub_id):
        # Only admin can update a subject
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        # Get new data from request
        data = request.get_json()
        # Find the subject by ID
        subject = Subject.query.filter_by(subject_id = sub_id).first()
        if not subject:
            return {'message': 'Subject does not exist'}, 404
        # Update subject's name and description
        subject.subject_name = data['subject_name']
        subject.subject_description = data['subject_description']
        db.session.commit()
        return {'message': 'Subject updated successfully'}, 200

    @jwt_required()
    def delete(self, sub_id):
        # Only admin can delete a subject
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        # Find the subject by ID
        subject = Subject.query.filter_by(subject_id = sub_id).first()
        if not subject:
            return {'message': 'Subject does not exist'}, 404
        # Remove subject from the database
        db.session.delete(subject)
        db.session.commit()
        return {'message': 'Subject deleted successfully'}, 200

# -------------------------------------------------------------------
# Chapter Management Resource (Admin Only): CRUD for chapters
# -------------------------------------------------------------------
class Add_Chapter(Resource):
    @jwt_required()
    def get(self):
        # Only admin can view all chapters
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        # Fetch all chapters from the database
        chapters = Chapter.query.all()
        chapter_json = []
        for chapter in chapters:
            chapter_json.append({
                "chapter_id": chapter.chapter_id,
                "chapter_name": chapter.chapter_name,
                "chapter_description": chapter.chapter_description
                })
        return chapter_json, 200
    
    @jwt_required()
    def post(self, sub_id):
        # Only admin can add a new chapter to a subject
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        data = request.get_json()
        # Get the subject by ID to link this chapter
        subject_id = Subject.query.filter_by(subject_id = sub_id).first()
        # Create and add the new chapter
        chapter = Chapter(chapter_name = data['chapter_name'],
                          chapter_description = data['chapter_description'], subject_id_of_chapter = subject_id.subject_id)
        db.session.add(chapter)
        db.session.commit()
        return {'message': 'Chapter added successfully'}, 200    
    
    @jwt_required()
    def put(self, chap_id):
        # Only admin can update a chapter
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        data = request.get_json()
        chapter = Chapter.query.filter_by(chapter_id = chap_id).first()
        if not chapter:
            return {'message': 'Chapter does not exist'}, 404
        # Update chapter name and description
        chapter.chapter_name = data['chapter_name']
        chapter.chapter_description = data['chapter_description']
        db.session.commit()
        return {'message': 'Chapter updated successfully'}, 200
    
    @jwt_required()
    def delete(self, chap_id):
        # Only admin can delete a chapter
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        chapter = Chapter.query.filter_by(chapter_id = chap_id).first()
        if not chapter:
            return {'message': 'Chapter does not exist'}, 404
        db.session.delete(chapter)
        db.session.commit()
        return {'message': 'Chapter deleted successfully'}, 200

# -------------------------------------------------------------------
# Quiz Management Resource (Admin Only): CRUD for quizzes
# -------------------------------------------------------------------
class Add_Quiz(Resource):
    @jwt_required()
    def get(self):
        # Only admin can view all quizzes
        current_user = get_jwt_identity()
        claims = get_jwt()
        user_id = claims['user_id']
        quizzes = Quiz.query.all()
        quiz_json = []
        for quiz in quizzes:
            attempts = None
            # If quiz is attempted, count attempts and set inactive if needed
            if quiz.quiz_is_attempted:
                attempts = Score.query.filter_by(quiz_id_of_score = quiz.quiz_id).count()
                if attempts is not None and attempts > 0:
                    quiz.quiz_is_active = False
            quiz_json.append({
                "quiz_id": quiz.quiz_id,
                "quiz_name": quiz.quiz_name,
                "quiz_description": quiz.quiz_description,
                "chapter_id_of_quiz": quiz.chapter_id_of_quiz,
                "quiz_is_active": quiz.quiz_is_active,
                "quiz_release_date": quiz.quiz_release_date.strftime("%Y-%m-%d"),
                "quiz_duration": quiz.quiz_duration.strftime("%H:%M:%S"),
                "quiz_is_attempted": quiz.quiz_is_attempted,
                "chapter": quiz.chapter.chapter_name,
                "subject": quiz.chapter.subject.subject_name,
            })
        return quiz_json, 200
            
    @jwt_required()
    def post(self):
        # Only admin can add a new quiz
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        data = request.get_json()
        # Get the chapter for this quiz
        chapter_id = Chapter.query.filter_by(chapter_id = data['chapter_id_of_quiz']).first()
        # Create and add the new quiz
        quiz = Quiz(quiz_name = data['quiz_name'],
                    quiz_description = data['quiz_description'],
                    chapter_id_of_quiz = chapter_id.chapter_id,
                    quiz_release_date = datetime.strptime(data['quiz_release_date'], '%Y-%m-%d').date(),
                    quiz_duration = datetime.strptime(data['quiz_duration'], '%H:%M:%S').time(),
                    quiz_is_attempted = data.get('quiz_is_attempted', None))
        db.session.add(quiz)
        db.session.commit()
        return {'message': 'Quiz added successfully'}, 200
    
    @jwt_required()
    def put(self, quiz_id):
        # Only admin can update a quiz
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        data = request.get_json()
        quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
        if not quiz:
            return {'message': 'Quiz does not exist'}, 404
        # Update quiz details
        quiz.quiz_name = data['quiz_name']
        quiz.quiz_description = data['quiz_description']
        quiz.chapter_id_of_quiz = data['chapter_id_of_quiz']
        quiz.quiz_release_date = datetime.strptime(data['quiz_release_date'], '%Y-%m-%d').date()
        quiz.quiz_duration = datetime.strptime(data['quiz_duration'], '%H:%M:%S').time()
        quiz.quiz_is_attempted = data['quiz_is_attempted']
        db.session.commit()
        return {'message': 'Quiz updated successfully'}, 200
    
    @jwt_required()
    def delete(self, quiz_id):
        # Only admin can delete a quiz
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
        if not quiz:
            return {'message': 'Quiz does not exist'}, 404
        db.session.delete(quiz)
        db.session.commit()
        return {'message': 'Quiz deleted successfully'}, 200

# -------------------------------------------------------------------
# Question Management Resource (Admin Only): CRUD for questions
# -------------------------------------------------------------------
class Add_Question(Resource):
    @jwt_required()
    def get(self, quiz_id):
        # Only admin can view all questions for a quiz
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        questions = Question.query.filter_by(quiz_id_of_question = quiz_id).all()
        question_json = []
        for question in questions:
            question_json.append({
                "question_id": question.question_id,
                "question_tag": question.question_tag,
                "question_text": question.question_text,
                "question_option1": question.question_option1,
                "question_option2": question.question_option2,
                "question_option3": question.question_option3,
                "question_option4": question.question_option4,
                "question_answer": question.question_answer
                })
        return question_json, 200
    
    @jwt_required()
    def post(self, quiz_id):
        # Only admin can add a new question to a quiz
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        data = request.get_json()
        # Get the chapter for this quiz
        chapter_id = Quiz.query.filter_by(quiz_id = quiz_id).first().chapter_id_of_quiz
        # Create and add the new question
        question = Question(chapter_id_of_question = chapter_id,
                            question_tag = data['question_tag'],
                            question_text = data['question_text'],
                            question_option1 = data['question_option1'],
                            question_option2 = data['question_option2'],
                            question_option3 = data['question_option3'],
                            question_option4 = data['question_option4'],
                            question_answer = data['question_answer'],
                            quiz_id_of_question = quiz_id)
        db.session.add(question)
        db.session.commit()
        return {'message': 'Question added successfully'}, 200
    
    @jwt_required()
    def put(self, question_id):
        # Only admin can update a question
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        data = request.get_json()
        question = Question.query.filter_by(question_id = question_id).first()
        if not question:
            return {'message': 'Question does not exist'}, 404
        # Update question details
        question.question_tag = data['question_tag']
        question.question_text = data['question_text']
        question.question_option1 = data['question_option1']
        question.question_option2 = data['question_option2']
        question.question_option3 = data['question_option3']
        question.question_option4 = data['question_option4']
        question.question_answer = data['question_answer']
        db.session.commit()
        return {'message': 'Question updated successfully'}, 200
    
    @jwt_required()
    def delete(self, question_id):
        # Only admin can delete a question
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        question = Question.query.filter_by(question_id = question_id).first()
        if not question:
            return {'message': 'Question does not exist'}, 404
        db.session.delete(question)
        db.session.commit()
        return {'message': 'Question deleted successfully'}, 200

# -------------------------------------------------------------------
# Export Scores Resource (User Only): Triggers background export task
# -------------------------------------------------------------------
class Export_Details(Resource):
    @jwt_required()
    def get(self):
        # Only regular users can export their scores
        current_user = get_jwt_identity()
        if current_user == "admin":
            return {'message': 'Only accessible to user'}, 401    
        claims = get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User does not exist'}, 404
        # Trigger Celery task to export scores
        export_scores.apply_async(args=[user_id])
        return {'message': 'Scores exported successfully'}, 200       

# -------------------------------------------------------------------
# Start Quiz Resource (User Only): Handles quiz attempt and submission
# -------------------------------------------------------------------
class StartQuiz(Resource):
    @jwt_required()
    def get(self, quiz_id):
        # Only regular users can attempt quizzes
        current_user = get_jwt_identity()
        if current_user == "admin":
            return {'message': 'Only accessible to user'}, 401    
        claims = get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User does not exist'}, 404
        quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
        if not quiz:
            return {'message': 'Quiz does not exist'}, 404
        # Check if user has already attempted this quiz
        if quiz.quiz_is_attempted:
            existing_attempt = Score.query.filter_by(user_id_of_score=user_id, quiz_id_of_score=quiz_id).first()
            if existing_attempt:
                return {'message': 'You can only attempt this quiz once'}, 403
        # Get all questions for this quiz
        questions = Question.query.filter_by(quiz_id_of_question = quiz_id).all()
        # Calculate time limit in seconds
        time_limit = quiz.quiz_duration.hour * 3600 + quiz.quiz_duration.minute * 60 + quiz.quiz_duration.second  
        quiz_data = {
            "quiz_id": quiz_id,
            "quiz_name": quiz.quiz_name,
            "time_limit": time_limit,
            "questions": [
                {
                    "question_id": question.question_id,
                    "question_tag": question.question_tag,
                    "question_text": question.question_text,
                    "question_option_a": question.question_option1,
                    "question_option_b": question.question_option2,
                    "question_option_c": question.question_option3,
                    "question_option_d": question.question_option4,
                    "question_answer": question.question_answer
            }for question in questions]
        }
        return quiz_data

    @jwt_required()
    def post(self, quiz_id):
        # Only regular users can submit quiz answers
        current_user = get_jwt_identity()
        if current_user == "admin":
            return {'message': 'Only accessible to user'}, 401    
        claims = get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User does not exist'}, 404
        quiz = Quiz.query.filter_by(quiz_id = quiz_id).first()
        if not quiz:
            return {'message': 'Quiz does not exist'}, 404
        # Check if user has already attempted this quiz
        if quiz.quiz_is_attempted:
            existing_attempt = Score.query.filter_by(user_id_of_score=user_id, quiz_id_of_score=quiz_id).first()
            if existing_attempt:
                return {'message': 'You can only attempt this quiz once'}, 403
        # Get chapter and subject for this quiz
        chapter = Chapter.query.get(quiz.chapter_id_of_quiz)
        subject = Subject.query.filter_by(subject_id = chapter.subject_id_of_chapter).first()
        # Get all questions for this quiz
        questions = Question.query.filter_by(quiz_id_of_question = quiz_id).all()
        data = request.get_json()
        score_of_user = 0
        maximum_score = len(questions)
        # Check each answer, increment score if correct
        for question in questions:
            user_marked_answer = data.get('question_answer',{}).get(str(question.question_id))
            user_marked_answer = user_marked_answer.strip().lower() if user_marked_answer else None
            question_answer = question.question_answer.strip().lower() if question.question_answer else None
            if user_marked_answer == question_answer:
                score_of_user += 1
        # Calculate percentage score
        score_percentage = (score_of_user / maximum_score) * 100
        timestamp = datetime.now().date()
        # Create a new Score record and save to database
        new_score = Score(user_id_of_score = user_id,
                          quiz_id_of_score = quiz_id,
                          subject_id_of_score = subject.subject_id,
                          chapter_id_of_score = chapter.chapter_id,
                          score_of_user = score_of_user,
                          maximum_score = maximum_score,
                          score_release_date = timestamp,
                          score_percentage = round(score_percentage,2))
        db.session.add(new_score)
        db.session.commit()
        return {'message': 'Quiz submitted successfully',
                 'score': score_of_user,
                   'maximum_score': maximum_score,
                     'score_percentage': score_percentage}, 200

# -------------------------------------------------------------------
# User Scorecard Resource (User Only): View all quiz scores
# -------------------------------------------------------------------
class User_Scorecard(Resource):
    @jwt_required()
    def get(self):    
        # Only regular users can view their scorecard
        current_user = get_jwt_identity()
        if current_user == "admin":
            return {'message': 'Only accessible to user'}, 401    
        claims = get_jwt()
        user_id = claims['user_id']
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User does not exist'}, 404
        # Fetch all scores for this user
        scores = Score.query.filter_by(user_id_of_score = user_id).all()
        result = []
        for score in scores:
            result.append({
               'subject_name': score.subject.subject_name,
               'chapter_name': score.chapter.chapter_name,
               'quiz_name': score.quiz.quiz_name,
               'score': score.score_of_user,
               'maximum_score': score.maximum_score,
               'percentage': score.score_percentage,
               'score_release_date': score.score_release_date.strftime('%Y-%m-%d')
            })
        return result, 200

# -------------------------------------------------------------------
# Admin Stats Resource: Platform-wide analytics for admin
# -------------------------------------------------------------------
class Admin_Stats(Resource):
    @jwt_required()
    def get(self):
        # Only admin can view platform stats
        current_user = get_jwt_identity()
        if current_user != "admin":  
            return {'message': 'Only accessible to admin'}, 401
        # Count subject-wise quiz attempts (for pie chart)
        subjectwise_attempts = (
            db.session.query(
                Subject.subject_name,
                db.func.count(Score.user_id_of_score)
            )
            .join(Score.quiz)
            .join(Quiz.chapter)
            .join(Chapter.subject)
            .group_by(Subject.subject_name)
            .all()
        )
        pie_labels = []
        pie_values = []
        for subject,count in subjectwise_attempts:
            if count > 0:
                pie_labels.append(subject)
                pie_values.append(count)
        # Count subject-wise top scores (for bar chart)
        topscorer = (
            db.session.query(
                Subject.subject_name,
                db.func.max(Score.score_percentage)
            )
            .join(Score.quiz)
            .join(Quiz.chapter)
            .join(Chapter.subject)
            .group_by(Subject.subject_name)
            .all()
        )
        bar_labels = []
        bar_values = []
        for subject,maxscore in topscorer:
            if maxscore > 0:
                bar_labels.append(subject)
                bar_values.append(maxscore)
        return {
            'pie_labels': pie_labels,
            'pie_values': pie_values, 
            'bar_labels': bar_labels, 
            'bar_values': bar_values}, 200

# -------------------------------------------------------------------
# User Stats Resource: Personal analytics for users
# -------------------------------------------------------------------
class User_Stats(Resource):
    @jwt_required()
    def get(self):
        # Only regular users can view their stats
        current_user = get_jwt_identity()
        if current_user == "admin":
            return {'message': 'Only accessible to user'}, 401
        claims = get_jwt()
        user_id = claims['user_id']

        # Subject-wise attempts by this user
        subjectwise_attempts = db.session.query(
            Subject.subject_name,
            db.func.count(Score.quiz_id_of_score)
        ).join(Score, Score.subject_id_of_score == Subject.subject_id
        ).filter(Score.user_id_of_score == user_id
        ).group_by(Subject.subject_name).all()

        pie_labels = []
        pie_values = []
        for subject, count in subjectwise_attempts:
            if count > 0:
                pie_labels.append(subject)
                pie_values.append(count)

        # Subject-wise top percentage scores for this user
        topscorer = db.session.query(
            Subject.subject_name,
            db.func.max(Score.score_percentage)
        ).join(Score, Score.subject_id_of_score == Subject.subject_id
        ).filter(Score.user_id_of_score == user_id
        ).group_by(Subject.subject_name).all()

        bar_labels = []
        bar_values = []
        for subject, maxscore in topscorer:
            if maxscore is not None:
                bar_labels.append(subject)
                bar_values.append(maxscore)

        return {
            'pie_labels': pie_labels,
            'pie_values': pie_values,
            'bar_labels': bar_labels,
            'bar_values': bar_values
        }, 200

# -------------------------------------------------------------------
# User Management Resource (Admin Only): View all non-admin users
# -------------------------------------------------------------------
class Manage_User(Resource):    
    @jwt_required()
    def get(self):
        # Only admin can view all users
        current_user = get_jwt_identity()
        if current_user != "admin":
            return {'message': 'Only accessible to admin'}, 401
        # Fetch all non-admin users
        users = User.query.filter_by(user_is_administrator = False).all()
        user_json = []
        for user in users:
            user_json.append({
                "user_id": user.user_id,
                "user_name": user.user_name,
                "user_email": user.user_email,
                "user_complete_name": user.user_complete_name,
                "user_education_level": user.user_education_level
                })
        return user_json, 200
