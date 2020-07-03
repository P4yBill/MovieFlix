from flask import (
    Blueprint, request, redirect, url_for, flash
)
from flask_wtf.csrf import validate_csrf, CSRFError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_required,
    logout_user,
    login_user
)
from wtforms import ValidationError
from ..models import User
from .db import db

auth_bp = Blueprint('auth', __name__)

users = db['Users']


@auth_bp.route('/login', methods=['POST'])
def login():
    token = request.form['csrf_token']
    try:
        validate_csrf(token)
    except CSRFError:
        flash('Csrf token invalid.')
        return redirect(url_for('auth_pages.login_page'))
    email = request.form.get('email')

    user = users.find_one({'email': email})
    password = request.form.get('password')

    if not user or not check_password_hash(user['password'], password):
        flash('Please check your login details.')
        return redirect(url_for('auth_pages.login_page'))

    login_retrieved_user(user)

    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['POST'])
def register():
    token = request.form['csrf_token']
    try:
        validate_csrf(token)
    except ValidationError:
        flash('Csrf token invalid.')
        return redirect(url_for('auth_pages.register_page'))
    email = request.form.get('email')

    user = users.find_one({'email': email})

    if user:  # if a user is found, we want to redirect back to register page so user can try again
        flash('User already exists. Please choose a different email')
        return redirect(url_for('auth.register'))

    name = request.form.get('name')
    password = request.form.get('password')
    category = 'user'
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    hashed_pass = generate_password_hash(password, method='sha256')

    users.insert_one({'email': email, 'name': name, 'password': hashed_pass, 'category': category, 'comments': []})

    user_to_login = {'email': email, 'name': name, 'category': category}
    login_retrieved_user(user_to_login)

    return redirect(url_for('main.index'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


def login_retrieved_user(user_retrieved):
    user = User()
    user.id = user_retrieved['email']
    user.name = user_retrieved['name']
    user.category = user_retrieved['category']

    login_user(user)
