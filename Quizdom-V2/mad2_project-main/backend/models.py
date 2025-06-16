from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy database object
db = SQLAlchemy()

# ---------------------
# User model/table
# ---------------------
# Stores all registered users.
# Each user has a unique name and email, a password, date of birth, full name,
# admin status, and education level.
# Linked to all quiz scores earned by the user.
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)
    user_dob = db.Column(db.Date, nullable=False)
    user_complete_name = db.Column(db.String(120), nullable=False)
    user_is_administrator = db.Column(db.Boolean, default=False)
    user_education_level = db.Column(db.String(120), nullable=False)

    scores = db.relationship('Score', back_populates='user', cascade="all, delete")

# ---------------------
# Subject model/table
# ---------------------
# Represents a subject (like Math or Science).
# Each subject has a unique name and description.
# Linked to its chapters and to all scores related to this subject.
class Subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(80), unique=True, nullable=False)
    subject_description = db.Column(db.String(120), nullable=False)

    chapters = db.relationship('Chapter', back_populates='subject', cascade="all, delete")
    scores = db.relationship('Score', back_populates='subject', cascade="all, delete")

# ---------------------
# Chapter model/table
# ---------------------
# Represents a chapter within a subject.
# Each chapter has a unique name and description, and belongs to a subject.
# Linked to its quizzes, questions, and all scores for this chapter.
class Chapter(db.Model):
    chapter_id = db.Column(db.Integer, primary_key=True)
    chapter_name = db.Column(db.String(80), unique=True, nullable=False)
    chapter_description = db.Column(db.String(120), nullable=False)
    subject_id_of_chapter = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False) 

    subject = db.relationship('Subject', back_populates='chapters')
    quizzes = db.relationship('Quiz', back_populates='chapter', cascade="all, delete")
    scores = db.relationship('Score', back_populates='chapter', cascade="all, delete")
    questions = db.relationship('Question', back_populates='chapter', cascade="all, delete")

# ---------------------
# Quiz model/table
# ---------------------
# Represents a quiz within a chapter.
# Each quiz has a unique name, description, release date, duration, and status flags.
# Linked to its questions and all scores for this quiz.
class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(80), unique=True, nullable=False)
    quiz_description = db.Column(db.String(120), nullable=False)
    chapter_id_of_quiz = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'), nullable=False)
    quiz_is_active = db.Column(db.Boolean, default=True)
    quiz_release_date = db.Column(db.DateTime, nullable = False)
    quiz_duration = db.Column(db.Time, nullable = False)
    quiz_is_attempted = db.Column(db.Boolean, nullable = True)

    chapter = db.relationship('Chapter', back_populates='quizzes')
    questions = db.relationship('Question', back_populates='quiz', cascade="all, delete")
    scores = db.relationship('Score', back_populates='quiz', cascade="all, delete")

# ---------------------
# Question model/table
# ---------------------
# Represents a question in a quiz.
# Stores the question text, four options, the correct answer, and tags.
# Linked to both the quiz and chapter it belongs to.
class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_tag = db.Column(db.String(120), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_option1 = db.Column(db.String(120), nullable=False)
    question_option2 = db.Column(db.String(120), nullable=False)
    question_option3 = db.Column(db.String(120), nullable=False)
    question_option4 = db.Column(db.String(120), nullable=False)
    question_answer = db.Column(db.String(120), nullable=False)
    quiz_id_of_question = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    chapter_id_of_question = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'), nullable=False)

    chapter = db.relationship('Chapter', back_populates='questions')
    quiz = db.relationship('Quiz', back_populates='questions')

# ---------------------
# Score model/table
# ---------------------
# Stores the result of a user's quiz attempt.
# Links to the user, quiz, subject, and chapter.
# Stores the score, max score, release date, and percentage.
class Score(db.Model):
    score_id = db.Column(db.Integer, primary_key=True)
    user_id_of_score = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    quiz_id_of_score = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'), nullable=False)
    subject_id_of_score = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)
    chapter_id_of_score = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'), nullable=False)
    score_of_user = db.Column(db.Integer, nullable=False)  
    maximum_score = db.Column(db.Integer, nullable=False)
    score_release_date = db.Column(db.DateTime, nullable = False)
    score_percentage = db.Column(db.Float, nullable = False) 

    user = db.relationship('User', back_populates='scores')
    subject = db.relationship('Subject', back_populates='scores')
    chapter = db.relationship('Chapter', back_populates='scores')
    quiz = db.relationship('Quiz', back_populates='scores')