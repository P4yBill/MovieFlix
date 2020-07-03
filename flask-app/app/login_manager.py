from functools import wraps

from flask import current_app, render_template
from werkzeug.exceptions import abort
from .models import User
from .routes.db import db
from flask_login import current_user

users = db['Users']


def manage_login(login_manager):
    # login_manager.login_view = "auth_pages.login_page"

    @login_manager.user_loader
    def user_loader(email):
        retrieved_user = users.find_one({'email': email})

        if not retrieved_user:
            return

        user = User()
        user.id = email
        user.name = retrieved_user['name']
        user.category = retrieved_user['category']

        return user

    @login_manager.unauthorized_handler
    def unauthorized():
        # do stuff
        return render_template("401.html")

def restricted(access_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user:
                return current_app.login_manager.unauthorized()
            elif not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            elif not current_user.category == access_level:
                return abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator
