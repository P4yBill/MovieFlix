import pymongo
from flask import request, Response
from ...login_manager import restricted
from flask_login import login_required
from ..db import db

movies = db['Movies']


class Movies(object):
    def __init__(self, blueprint=None):
        if blueprint is not None:
            self.register_movies_routes(blueprint)

    def register_movies_routes(self, bp):
        @bp.route('/movies', methods=['POST'])
        def create_movie():
            return {'response': 200, 'method': request.endpoint}
