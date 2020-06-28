from json import dumps

from bson import ObjectId, json_util
from bson.errors import InvalidId
from flask import request, Response
from ..utils import wrong_res
from ...login_manager import restricted
from flask_login import login_required, current_user
from ..db import db

movies = db['Movies']
users = db['Users']


class Comments(object):
    def __init__(self, blueprint=None):
        if blueprint is not None:
            self.register_comments_routes(blueprint)

    def register_comments_routes(self, bp):
        @bp.route('/movies/<string:movie_id>/comments', methods=['POST'])
        @login_required
        def create_comment(movie_id):
            res_obj = {}
            if request.is_json:
                content = request.get_json()
            else:
                return wrong_res("Bad Request")

            if "comment" not in content:
                return wrong_res("Wrong params")

            if not str(content["comment"]):
                return wrong_res("Wrong params")

            if content["comment"] == "":
                return wrong_res("Wrong params")

            movie = movies.find_one({"_id": ObjectId(movie_id)})

            if not movie:
                res_obj = {"error": "Movie could not be found"}
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            email = current_user.id
            has_comment = users.find_one({"email": email, "comments": {"$elemMatch": {"movie_id": ObjectId(movie_id)}}})

            if has_comment:
                res_obj = {"error": "You have already commented on this movie"}
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            comment = content["comment"]

            try:
                users.update(
                    {"email": email},
                    {"$push": {"comments": {
                        "movie_id": ObjectId(movie_id),
                        "comment": comment
                    }}}
                )

                movies.update(
                    {"_id": ObjectId(movie_id)},
                    {"$push": {"comments": {
                        "user_id": email,
                        "comment": comment
                    }}}
                )

                res_obj["error"] = "OK"
                return Response(json_util.dumps(res_obj), status=200, mimetype="application/json")
            except Exception as e:
                res_obj["error"] = "Could not insert the comment."
                return Response(dumps(res_obj), status=500, mimetype='application/json')

        @bp.route('/movies/<string:movie_id>/comments', methods=['DELETE'])
        @login_required
        def delete_comment(movie_id):
            res_obj = {}
            if request.is_json:
                content = request.get_json()
            else:
                return wrong_res("Bad Request")

            if "user_id" not in content:
                return wrong_res("Wrong params")

            if not str(content["user_id"]):
                return wrong_res("Wrong params")
            try:
                movie = movies.find_one({"_id": ObjectId(movie_id)})
                if not movie:
                    return wrong_res("Movie could not be found.")
            except InvalidId:
                return wrong_res("Movie could not be found.")

            user_id = content["user_id"]

            # email = current_user.id
            current_user = {"category": "user", "id": "vvv@gmail.com"}

            if current_user.id != user_id:
                user = users.find_one({"email" : user_id})
                print(user)
                if not user:
                    return wrong_res("User could not be found.")

                if current_user.category != "admin":
                    res_obj = {"error": "You dont have the rights to do this action."}
                    return Response(dumps(res_obj), status=403, mimetype="application/json")

            has_comment = users.find_one({"email": user_id, "comments": {"$elemMatch": {"movie_id": ObjectId(movie_id)}}})

            if not has_comment:
                res_obj = {"error": "Comment does not exist"}
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            try:
                users.update(
                    {"email": user_id},
                    {"$pull": {"comments": {
                        "movie_id": ObjectId(movie_id),
                    }}}
                )

                movies.update(
                    {"_id": ObjectId(movie_id)},
                    {"$pull": {"comments": {
                        "user_id": user_id,
                    }}}
                )

                res_obj["error"] = "OK"
                return Response(json_util.dumps(res_obj), status=200, mimetype="application/json")
            except Exception as e:
                res_obj["error"] = "Could not insert the comment."
                return Response(dumps(res_obj), status=500, mimetype='application/json')