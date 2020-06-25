from bson import json_util
from flask import request, Response
from ..db import db
from ...login_manager import restricted
from flask_login import login_required

users = db['Users']


class Users(object):
    def __init__(self, blueprint=None):
        if blueprint is not None:
            self.register_user_routes(blueprint)

    def register_user_routes(self, bp):
        @bp.route('/users', methods=['GET'])
        @restricted(access_level="admin")
        @login_required
        def get_user():
            res_obj = {}
            try:
                users_retrieved = users.find({'category': 'user'}, {'email', 'name', 'category'})
                users_as_list = list(users_retrieved)
                res_obj["data"] = users_as_list
                res_obj["error"] = ""
                return Response(json_util.dumps(res_obj), status=200, mimetype="application/json")
            except Exception as e:
                res_obj["error"] = "Could not retrieve users"
                res_obj["data"] = []
                return Response(json_util.dumps(res_obj), status=500, mimetype='application/json')

        @bp.route('/users', methods=['DELETE'])
        @login_required
        def delete_user():
            res_obj = {"error": ""}

            if request.is_json:
                content = request.get_json()
            else:
                res_obj["error"] = "Bad Request"
                return Response(json_util.dumps(res_obj), status=500, mimetype="application/json")

            if "email" not in content:
                res_obj["error"] = "Wrong params"
                return Response(json_util.dumps(res_obj), status=500, mimetype="application/json")

            user_mail = content["email"]

            try:
                user_to_delete = users.find_one({"email": user_mail})
                if user_to_delete:
                    users.delete_one(user_to_delete)

                    res_obj["error"] = "OK"
                    return Response(json_util.dumps(res_obj), status=200, mimetype="application/json")
                else:
                    res_obj["error"] = "We did not find the user"
                    return Response(json_util.dumps(res_obj), status=500, mimetype='application/json')
            except Exception as e:
                res_obj["error"] = "User could not be deleted"
                return Response(json_util.dumps(res_obj), status=500, mimetype='application/json')

        @bp.route('/users', methods=['PUT'])
        @restricted(access_level="admin")
        @login_required
        def update_user():
            res_obj = {"error": ""}

            if request.is_json:
                content = request.get_json()
            else:
                res_obj["error"] = "Bad Request"
                return Response(json_util.dumps(res_obj), status=500, mimetype="application/json")

            if "email" not in content or "category" not in content:
                res_obj["error"] = "Wrong params"
                return Response(json_util.dumps(res_obj), status=500, mimetype="application/json")
            user_mail = content["email"]
            user_category = content["category"]
            user_to_delete = users.find_one({"email" : user_mail})

            if not user_to_delete:
                res_obj["error"] = "Could not find the user"
                return Response(json_util.dumps(res_obj), status=500, mimetype='application/json')

            try:
                users.update_one({"email": user_mail}, {"$set": {"category": user_category}})
                res_obj["error"] = "OK"
                return Response(json_util.dumps(res_obj), status=200, mimetype="application/json")
            except Exception as e:
                res_obj["error"] = "User could not be updated"
                return Response(json_util.dumps(res_obj), status=500, mimetype='application/json')
