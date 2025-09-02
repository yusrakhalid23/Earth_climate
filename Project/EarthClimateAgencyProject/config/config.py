import os
from dotenv import load_dotenv

# Load environment variables from .env file (optional but recommended)
load_dotenv()

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # MongoDB connection URI
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Email configuration (for sending emails)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Enable/Disable debug mode
    DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Default to True for development
