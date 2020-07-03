from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from ..db import db
from ...login_manager import restricted

movies_bp = Blueprint('movies_views', __name__, template_folder="templates", static_folder="static",
                      static_url_path='/movies/static')
movies_db = db['Movies']


@movies_bp.route('/movies', endpoint='movies_page', methods=['GET'])
@login_required
def movies():
    movies_re = movies_db.find()
    movies = list(movies_re)

    return render_template('movies/movies.html', movies=movies)


@movies_bp.route('/movies/view/<string:movie_id>', endpoint='movie_view', methods=['GET'])
@login_required
def movie_view(movie_id):
    try:
        movie = movies_db.find_one({"_id": ObjectId(movie_id)})
    except InvalidId:
        flash("No movie found with id: " + movie_id, category='error')
        return redirect(url_for('movies_page'))

    if not movie:
        flash("No movie found with id: " + movie_id, category='error')
        return redirect(url_for('movies_page'))

    return render_template('movies/movie_view.html', movie=movie)


@movies_bp.route('/movies/create', endpoint='movie_create', methods=['GET'])
@restricted(access_level="admin")
@login_required
def movie_create():
    return render_template('movies/movie_create.html')


@movies_bp.route('/movies/edit/<string:movie_id>', endpoint='movie_edit', methods=['GET'])
@restricted(access_level="admin")
@login_required
def movie_create(movie_id):
    try:
        movie = movies_db.find_one({"_id": ObjectId(movie_id)})
    except InvalidId:
        flash("No movie found with id: " + movie_id, category='error')
        return redirect(url_for('movies_page'))

    if not movie:
        flash("No movie found with id: " + movie_id, category='error')
        return redirect(url_for('movies_page'))

    return render_template('movies/movie_edit.html', movie=movie)
