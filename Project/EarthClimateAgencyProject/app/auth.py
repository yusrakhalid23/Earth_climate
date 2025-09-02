from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash  # For hashing passwords
from .mongo import mongo
import re  # Regular expressions for email validation

auth = Blueprint('auth', __name__)

# Route for Login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = mongo.db.users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):  # Use hashed password comparison
            session['username'] = username  # Store username in session
            next_page = request.args.get('next')  # Get the next page
            return redirect(next_page or url_for('main.index'))  # Redirect to next or index
        else:
            flash('Login failed. Please check your username or password.')

    return render_template('login.html')

# Route for Registration
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Basic Validation: Check if the username already exists
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists. Please choose a different one.')
        # Email validation regex
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email format.')
        # Check if password length is sufficient (minimum 6 characters)
        elif len(password) < 6:
            flash('Password should be at least 6 characters long.')
        else:
            hashed_password = generate_password_hash(password)  # Hash the password before saving
            mongo.db.users.insert_one({'username': username, 'email': email, 'password': hashed_password})
            flash('Registration successful! You can now log in.')
            return redirect(url_for('auth.login'))

    return render_template('register.html')

# Route for Logout
@auth.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('main.index'))
