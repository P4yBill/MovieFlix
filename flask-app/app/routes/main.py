from flask import (render_template, request, Blueprint)
import json
import flask_login
from ..login_manager import restricted
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db = client['MovieFlix']
movies = db['Movies']

main_bp = Blueprint('main', __name__)


@main_bp.route('/home', methods=['GET'])
@main_bp.route('/', endpoint='index', methods=['GET'])
def index():
    return render_template('home.html')


@main_bp.route('/<name>')
def hello_name(name):
    return f"Hello {request.endpoint}!\n"


@main_bp.route("/getInfo", methods=['GET'])
def get_info():
    print("int info get")

    return {'response': 200, 'method': 'GET'}


@main_bp.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@main_bp.route("/getInfo", methods=['POST'])
def get_info_post():
    print("int info post")
    try:
        print(request.json)
        print("Kalispera")
        params = {
            'thing1': request.values.get('name'),
        }
        print(params)
    except AttributeError:
        print("something wrong")

    data = json.loads('{"data": {"name": "testing"}}')
    movies_list = movies.find()
    for movie in movies_list:
        print(movie)
    data['method'] = 'POST'
    data['response'] = 201
    return data


@main_bp.route("/admin", endpoint='admin_panel', methods=['GET'])
@restricted(access_level="admin")
@flask_login.login_required
def admin_panel():
    print('Admin panel')
    return {'page': 'Admin panel', 'method': 'GET'}
