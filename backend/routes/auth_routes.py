# Author: Kenneth Kang
# Modified by: AI Assistant (Added bonus feature: user profile endpoint)

# Import necessary modules from Flask and other packages
from flask import Blueprint, jsonify, request, session
import re

# Create a Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

# In-memory user storage (dictionary)
# Structure: {username: {password, email, first_name, last_name, dob}}
users = {}

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint to handle user registration.
    Expects JSON payload with 'username', 'password', 'confirm_password', 'first_name', 'last_name', 'dob', and 'email'.
    Password must contain at least one uppercase, one lowercase, one number, and one special symbol.
    The email is auto-generated as <username>@ka-tch.com.
    """
    data = request.get_json()
    required_fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'dob', 'email')
    # Validate all required fields are present
    if not data or not all(key in data for key in required_fields):
        return jsonify({'error': 'Invalid request data'}), 400
    username = data['username']
    password = data['password']
    confirm_password = data['confirm_password']
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    # Automatically generate email address ending with @ka-tch.com
    email = f"{username}@ka-tch.com"
    # Password validation: check match and strength
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match.'}), 400
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).+$', password):
        return jsonify({'error': 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special symbol.'}), 400
    if username in users:
        return jsonify({'error': 'User already exists'}), 409
    # Store user data in memory
    users[username] = {
        'password': password,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'dob': dob
    }
    return jsonify({'message': 'Registration successful', 'user': username, 'email': email}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint to handle user login.
    Expects JSON payload with 'username' and 'password'.
    Sets session['user'] if login is successful.
    """
    data = request.get_json()
    if not data or not all(key in data for key in ('username', 'password')):
        return jsonify({'error': 'Invalid request data'}), 400
    username = data['username']
    password = data['password']
    # Check credentials
    user = users.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid username or password'}), 401
    session['user'] = username
    return jsonify({'message': 'Login successful', 'user': username}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint to handle user logout.
    Clears the session (removes 'user').
    """
    session.pop('user', None)
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    """
    Endpoint to check the authentication status.
    Returns the current user if logged in, otherwise returns unauthenticated status.
    """
    user = session.get('user')
    if user:
        return jsonify({'status': 'authenticated', 'user': user}), 200
    else:
        return jsonify({'status': 'unauthenticated'}), 401

# BONUS FEATURE: User Profile Endpoint
@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Endpoint to get the current user's profile information.
    Returns user details including email, first name, last name, and date of birth.
    """
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    username = session['user']
    user_data = users.get(username, {})
    return jsonify({
        'username': username,
        'email': user_data.get('email', f'{username}@ka-tch.com'),
        'first_name': user_data.get('first_name', ''),
        'last_name': user_data.get('last_name', ''),
        'dob': user_data.get('dob', '')
    }), 200



