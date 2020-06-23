from flask import request


class Users(object):
    def __init__(self, blueprint=None):
        if blueprint is not None:
            self.register_user_routes(blueprint)

    def register_user_routes(self, bp):
        @bp.route('/users', methods=['GET'])
        def get_user():
            return {'response': 200, 'method': request.endpoint + request.method}


