from json import dumps

from bson import ObjectId, json_util
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
        @restricted(access_level="admin")
        @login_required
        def create_movie():
            if request.is_json:
                content = request.get_json()
            else:
                res_obj = {"error": "Bad Request"}
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            movie = get_movie(content, create=True)

            if movie:
                movies.insert_one(movie)

                res_obj = {"error": "OK"}
                return Response(dumps(res_obj), status=200, mimetype="application/json")
            else:
                res_obj = {"error": "You have to specify the title and at least on actor"}
                return Response(dumps(res_obj), status=500, mimetype="application/json")

        @bp.route('/movies', methods=['GET'])
        @login_required
        def get_movies():
            res_obj = {"error": ""}
            print(request.is_json)
            if request.is_json:
                content = request.get_json()
            else:
                res_obj["error"] = "Bad Request"
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            movie_from_params = get_movie_params(content)

            try:
                movies_retrieved = movies.find(movie_from_params)
                movies_as_list = list(movies_retrieved)
                print(movies_as_list)
                res_obj["error"] = "OK"
                res_obj["data"] = movies_as_list
                return Response(json_util.dumps(res_obj), status=200, mimetype="application/json")
            except Exception as e:
                res_obj["error"] = "Could not retrieve movies"
                res_obj["data"] = []
                return Response(dumps(res_obj), status=500, mimetype='application/json')

        @bp.route('/movies', methods=['PUT'])
        @restricted(access_level="admin")
        @login_required
        def update_movie():
            res_obj = {"error": ""}

            if request.is_json:
                content = request.get_json()
            else:
                res_obj["error"] = "Bad Request"
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            if "id" not in content:
                res_obj["error"] = "Wrong params"
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            movie_id = content["id"]
            movie_from_params = get_movie(content)

            if movie_from_params:
                try:
                    movies.update_one({"_id": ObjectId(movie_id)}, {"$set": movie_from_params})
                    res_obj["error"] = "OK"
                    return Response(dumps(res_obj), status=200, mimetype="application/json")
                except Exception as e:
                    res_obj["error"] = "Movie could not be updated"
                    return Response(dumps(res_obj), status=500, mimetype='application/json')
            else:
                res_obj = {"error": "You have to specify the title and at least on actor"}
                return Response(dumps(res_obj), status=500, mimetype="application/json")

        @bp.route('/movies', methods=['DELETE'])
        @restricted(access_level="admin")
        @login_required
        def delete_movie():
            res_obj = {"error": ""}

            if request.is_json:
                content = request.get_json()
            else:
                res_obj["error"] = "Bad Request"
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            if "title" not in content:
                res_obj["error"] = "Wrong params"
                return Response(dumps(res_obj), status=500, mimetype="application/json")

            movie_title = content["title"]

            try:
                # find the older movies by title
                movie_to_delete = movies.find({"title": movie_title}).sort("year", 1).limit(1)
                if movie_to_delete.count() == 1:
                    # get the first movie from the cursor
                    movie_to_delete = movie_to_delete[0]
                    movies.delete_one(movie_to_delete)

                    res_obj["error"] = "OK"
                    return Response(dumps(res_obj), status=200, mimetype="application/json")
                else:
                    res_obj["error"] = "Movie could not be deleted"
                    return Response(dumps(res_obj), status=500, mimetype='application/json')
            except Exception as e:
                res_obj["error"] = "Movie could not be deleted"
                return Response(dumps(res_obj), status=500, mimetype='application/json')


def get_movie(movie, create=False):
    required_fields = ['title', 'actors']
    fields = ['title', 'year', 'description', 'actors']

    movie_to_send = {}
    if all(name in movie for name in required_fields):
        if isinstance(movie['actors'], list) and isinstance(movie['title'], str) and len(movie['actors']):
            for key in required_fields:
                movie_to_send[key] = movie[key]
            for key in fields:
                if key in movie:
                    movie_to_send[key] = movie[key]
            if create:
                movie_to_send["comments"] = []
                movie_to_send["rating"] = 0

    return movie_to_send


def get_movie_params(movie):
    fields = ['title', 'year', 'actors']

    movie_to_send = {}
    for key in fields:
        if key in movie:
            movie_to_send[key] = movie[key]

    if "actors" in movie_to_send:
        movie_to_send["actors"] = {"$all": movie_to_send["actors"]}

    return movie_to_send
