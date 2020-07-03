from flask import Blueprint, render_template
from flask_login import login_required
from ..db import db

admin_panel_pb = Blueprint('admin_panel', __name__, template_folder="templates", static_folder="static",
                           static_url_path='/admin_panel/static')
users_db = db['Users']


@admin_panel_pb.route('/admin_panel', endpoint='index', methods=['GET'])
@login_required
def admin():
    simple_users = users_db.find({"category": "user"})
    simple_users = list(simple_users)

    return render_template('admin_panel/admin_panel.html', users=simple_users)
