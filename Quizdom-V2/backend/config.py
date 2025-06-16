from datetime import timedelta
from flask_caching import Cache

# Initialize the cache object (will be configured later with app)
cache = Cache()

# Base configuration class
class Config:
    DEBUG = False                 # Don't show debug info by default
    TESTING = False               # Not in testing mode by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables extra tracking to save resources

# Configuration for local development
class LocalConfig(Config):
    DEBUG = True                  # Show debug info (for development)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quizdom.db'  # Use a local SQLite database
    SECURITY_PASSWORD_HASH = 'bcrypt'                 # Use bcrypt for password hashing
    SECURITY_PASSWORD_SALT = 'salt'                   # Salt for hashing passwords
    JWT_SECRET_KEY = 'secret'                         # Key for signing JWT tokens
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)      # JWT tokens expire after 1 day

    # Redis cache configuration
    CACHE_TYPE = 'redis'                              # Use Redis for caching
    CACHE_REDIS_HOST = 'localhost'                    # Redis server is on local machine
    CACHE_REDIS_PORT = 6379                           # Default Redis port
    CACHE_REDIS_DB = 0                                # Use Redis database 0
    CACHE_REDIS_URL = 'redis://localhost:6379'        # Full Redis URL
    CACHE_DEFAULT_TIMEOUT = 300                       # Default cache timeout is 5 minutes

    # Email server configuration
    MAIL_SERVER = 'localhost'                         # Email server is on local machine
    MAIL_PORT = 587                                   # Port for sending emails (TLS)
    MAIL_USE_TLS = True                               # Use TLS for secure email sending
    MAIL_EMAIL = 'admin@gmail.com'                    # Default email address for sending emails
    MAIL_PASSWORD = 'admin123'                        # Password for the email account
