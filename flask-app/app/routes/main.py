from flask import (render_template, Blueprint)

main_bp = Blueprint('main', __name__)


@main_bp.route('/home', methods=['GET'])
@main_bp.route('/', endpoint='index', methods=['GET'])
def index():
    return render_template('home.html')