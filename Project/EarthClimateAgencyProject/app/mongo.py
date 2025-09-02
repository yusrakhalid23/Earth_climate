from flask_pymongo import PyMongo
from flask import current_app as app

# Initialize the PyMongo object to interact with MongoDB
mongo = PyMongo()

# Function to initialize PyMongo with Flask app
def init_app(app):
    mongo.init_app(app)
    print("MongoDB connected successfully!")

# Example of how you might use this:
# In your main `app.py`, you'll call the init_app function to initialize the MongoDB connection with Flask

