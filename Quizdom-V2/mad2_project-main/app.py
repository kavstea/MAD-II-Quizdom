# Importing necessary libraries and modules
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import datetime
from passlib.hash import bcrypt

# Importing database models and API resources
from backend.models import db, User
from backend.api import (
    User_Login, User_Signup, Add_Subject, Add_Chapter, Add_Quiz, Add_Question,
    Export_Details, StartQuiz, Admin_Stats, User_Stats, User_Scorecard, Manage_User
)
from backend.config import cache
from backend.worker import *
from backend.task import *

# Factory function to create and configure the Flask app
def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.LocalConfig')  # Load configuration
    db.init_app(app)         # Initialize SQLAlchemy with app
    cache.init_app(app)      # Initialize cache with app
    return app

# Function to ensure an admin user exists in the database
def admin():
    admin = User.query.filter_by(user_is_administrator=True).first()  # Look for existing admin
    if not admin:
        admin = User(
            user_name="admin",
            user_email="admin@gmail.com",
            user_password=bcrypt.hash("admin123"),  # Hash the default password
            user_dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
            user_complete_name="Admin",
            user_is_administrator=True,
            user_education_level="B.Tech"
        )
        db.session.add(admin)   # Add new admin to the session
        db.session.commit()     # Commit changes to the database

# Initialize the Flask app and extensions
app = create_app()
api = Api(app)              # Set up RESTful API
CORS(app)                   # Enable CORS for all routes
jwt = JWTManager(app)       # Set up JWT authentication

# Application context for initializing Celery, database, and admin user
with app.app_context():
    celery = celery_init_app(app)                     # Initialize Celery for background tasks
    celery.conf.beat_schedule = CeleryConfig.beat_schedule  # Set up periodic tasks
    db.create_all()                                   # Create all database tables
    admin()                                           # Ensure admin user exists

# Basic route for testing if the server is running
@app.get('/')
def index():
    return "Hello World"

# Route to test caching; returns current time, cached for 10 seconds
@app.get('/test')
@cache.cached(timeout=10)
def test():
    return {'Time': str(datetime.now())}

# Registering API resources/endpoints with their routes
api.add_resource(User_Login, '/login')
api.add_resource(User_Signup, '/signup')
api.add_resource(Add_Subject, '/add_subject/get', '/add_subject/post', '/edit_subject/<int:sub_id>', '/delete_subject/<int:sub_id>')
api.add_resource(Add_Chapter, '/add_chapter/get', '/add_chapter/<int:sub_id>', '/edit_chapter/<int:chap_id>', '/delete_chapter/<int:chap_id>')
api.add_resource(Add_Quiz, '/add_quiz', '/edit_quiz/<int:quiz_id>', '/delete_quiz/<int:quiz_id>', '/get_quiz')
api.add_resource(Add_Question, '/add_question/<int:quiz_id>', '/edit_question/<int:question_id>', '/delete_question/<int:question_id>', '/get_questions/<int:quiz_id>')
api.add_resource(Export_Details, '/export_details')
api.add_resource(StartQuiz, '/start_quiz/<int:quiz_id>')
api.add_resource(Admin_Stats, '/admin_stats')
api.add_resource(User_Stats, '/user_stats')
api.add_resource(User_Scorecard, '/user_scorecard')
api.add_resource(Manage_User, '/manage_user')

# Run the Flask development server if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)

