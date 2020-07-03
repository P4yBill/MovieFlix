from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
auth_pages = Blueprint('auth_pages', __name__, template_folder="templates")


@auth_pages.route('/register', endpoint='register_page', methods=['GET'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('auth_pages/register.html')


@auth_pages.route('/login', endpoint='login_page', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('auth_pages/login.html')
