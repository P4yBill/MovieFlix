from json import dumps
from bson import ObjectId, json_util
from bson.errors import InvalidId
from flask import request, Response, flash, render_template, redirect, url_for
from ..utils import wrong_res
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
            # if request.is_json:
            #     content = request.get_json()
            # else:
            #     res_obj = {"error": "Bad Request"}
            #     return Response(dumps(res_obj), status=500, mimetype="application/json")
            data = request.form
            if not data:
                flash('Could not create movie. Please try again.', 'danger')
                return redirect(url_for("movies_views.movie_create"))

            movie = get_movie_create(data)

            if bool(movie):
                print(movie);
                movies.insert_one(movie)

                # res_obj = {"error": "OK"}
                # return Response(dumps(res_obj), status=200, mimetype="application/json")
                flash('Movie created successfully', 'success')
                return redirect(url_for("movies_views.movie_create"))
            else:
                flash('Could not create movie. Please check your input', 'danger')
                return redirect(url_for("movies_views.movie_create"))
                # res_obj = {"error": "Params are incorrect. Tip: you have to specify the title and at least one actor"}
                # return Response(dumps(res_obj), status=500, mimetype="application/json")

        @bp.route('/movies', methods=['GET'])
        @login_required
        def get_movies():
            # res_obj = {"error": ""}
            movies_as_list = []

            movie_from_params = get_movie_params()

            try:
                movies_retrieved = movies.find(movie_from_params)
                movies_as_list = list(movies_retrieved)

                return render_template('movies/movies.html', movies=movies_as_list)
                # res_obj["error"] = "OK"
                # res_obj["data"] = movies_as_list
                # return Response(json_util.dumps(res_obj), status=200, mimetype="application/json")
            except Exception as e:
                flash('Could not retrieve movies. Please check your criteria and try again.', 'error')
                return render_template('movies/movies.html', movies=movies_as_list)
                # res_obj["error"] = "Could not retrieve movies. Please check your criteria and try again."
                # res_obj["data"] = []
                # return Response(dumps(res_obj), status=500, mimetype='application/json')

        @bp.route('/movies', methods=['PUT'])
        @restricted(access_level="admin")
        @login_required
        def update_movie():
            res_obj = {"error": ""}

            # if request.is_json:
            #     content = request.get_json()
            # else:
            #     res_obj["error"] = "Bad Request"
            #     return Response(dumps(res_obj), status=500, mimetype="application/json")

            # if "id" not in content:
            #     res_obj["error"] = "Wrong params"
            #     return Response(dumps(res_obj), status=500, mimetype="application/json")

            params = request.form

            if not params:
                return wrong_res("Bad Request")

            movie_id = params.get('movie_id')
            if not movie_id:
                return wrong_res("Wrong params")

            try:
                movie_to_update = movies.find_one({"_id": ObjectId(movie_id)})
            except InvalidId:
                return wrong_res("Wrong params")

            if not movie_to_update:
                return wrong_res("Wrong params")

            movie_new = get_movie_create(params)

            if movie_new:
                try:
                    movies.update_one({"_id": ObjectId(movie_id)}, {"$set": movie_new})

                    res_obj["error"] = "OK"
                    return Response(dumps(res_obj), status=200, mimetype="application/json")
                except Exception as e:
                    return wrong_res("Movie could not be updated")
            else:
                return wrong_res("Please check your input.")

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

                if movie_to_delete.count() > 0:
                    # get the first movie from the cursor
                    movie_to_delete = movie_to_delete[0]
                    movies.delete_one(movie_to_delete)

                    message = "Movie with title " + movie_to_delete['title'] + " and year " + \
                              str(movie_to_delete['year']) + " deleted successfully"

                    flash(message, category='success')
                    res_obj["error"] = "OK"
                    return Response(dumps(res_obj), status=200, mimetype="application/json")
                else:
                    res_obj["error"] = "Movie could not be deleted"
                    return Response(dumps(res_obj), status=500, mimetype='application/json')
            except Exception as e:
                res_obj["error"] = "Movie could not be deleted"
                return Response(dumps(res_obj), status=500, mimetype='application/json')


def get_movie_create(data):
    movie = {"title": request.form.get('title')}

    year = data.get('year')
    movie["description"] = data.get('description')
    actors = get_actors_array(data.get('actors'))

    if year is not None:
        if year.isnumeric():
            movie["year"] = int(year)
        else:
            movie["year"] = None

    if movie["title"] is None:
        return {}
    else:
        # we do not want a movie with title as spaces only
        movie["title"] = movie["title"].rstrip().lstrip()
        if not movie["title"]:
            return {}

    if not actors:
        return {}
    else:
        movie["actors"] = actors

    movie["rating"] = 0
    movie["comments"] = []

    return movie


def get_movie(movie, create=False):
    required_fields = ['title', 'actors']
    fields = ['title', 'year', 'description', 'actors']

    movie_to_send = {}
    if all(name in movie for name in required_fields):

        if isinstance(movie['actors'], list) and isinstance(movie['title'], str) and len(movie['actors']):
            if not actors_params_correct(movie['actors']):
                return
            for key in required_fields:
                if movie[key] is '':
                    return {}
                movie_to_send[key] = movie[key]
            for key in fields:
                if key in movie:
                    movie_to_send[key] = movie[key]
            if create:
                movie_to_send["comments"] = []
                movie_to_send["rating"] = 0

    return movie_to_send


def get_movie_params():
    # actors will be a string not an array
    fields = ['title', 'year', 'actors']

    movie_to_send = {}
    for key in fields:
        get_param = request.args.get(key)

        if get_param is not None and get_param != "":
            if get_param.isnumeric():
                get_param = int(get_param)
            if key == "actors":
                get_param = get_actors_array(get_param)
            movie_to_send[key] = get_param

    return movie_to_send


def get_actors_array(actors):
    if actors is None:
        return []
    actors_array = actors.split(",")
    # remove the whitespace at the beginning and at the end of each actor
    for i, actor in enumerate(actors_array):
        actors_array[i] = actor.rstrip().lstrip()
    if actors_params_correct(actors_array):
        return actors_array
    else:
        return []


def actors_params_correct(arr: list):
    try:
        for val in arr:
            if val.isnumeric():
                return False
            if not val:
                return False
    except ValueError:
        return False

    return True
