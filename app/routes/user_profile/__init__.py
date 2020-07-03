from flask import Blueprint, render_template
from flask_login import login_required
from ..db import db

user_profile_pb = Blueprint('user_profile', __name__, template_folder="templates", static_folder="static",
                           static_url_path='/user_profile/static')
users_db = db['Users']


@user_profile_pb.route('/profile', endpoint='index', methods=['GET'])
@login_required
def user_profile():
    return render_template('user_profile/user_profile.html')
