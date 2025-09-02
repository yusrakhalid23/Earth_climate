from flask import Flask
from .mongo import mongo
from .auth import auth as auth_blueprint
from .feedback import feedback_bp as feedback_blueprint
from .main import main as main_blueprint
from .notifications import notifications_bp as notifications_blueprint
from flask_mail import Mail

def create_app():
    # Create the Flask app instance
    app = Flask(__name__, static_folder='static')

    # Load configuration from config.py file
    app.config.from_object('config.config.Config')

    # Configure mail server
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Put your actual email
    app.config['MAIL_PASSWORD'] = 'your-email-password'  # Put your email password
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

    # Initialize MongoDB
    mongo.init_app(app)

    # Initialize Flask-Mail
    mail = Mail(app)

    # Register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(feedback_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(notifications_blueprint)

    # Error Handling for 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return 'This page does not exist!', 404

    # Error Handling for 500 - Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(e):
        return 'Internal Server Error!', 500

    return app
