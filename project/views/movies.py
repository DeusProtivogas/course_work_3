from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services import MoviesService
from project.setup_db import db

movies_ns = Namespace("movies")


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.response(200, "OK")
    def get(self):
        """Get all movies"""


        # if request.values.get("status") == "new":
        #     all_movies = sorted(all_movies, key=lambda x: x['year'], reverse=True)
        #
        # if request.values.get("page"):
        #     page = int(request.values.get("page"))
        #     all_movies = all_movies[12 * (page - 1): 12 * page]

        page = request.args.get("page")
        status = request.args.get("status")

        filters = {
            "page": page,
            "status": status,
        }

        all_movies = MoviesService(db.session).get_all_movies(filters)


        return all_movies


@movies_ns.route("/<int:movie_id>")
class MovieView(Resource):
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Movie not found")
    def get(self, movie_id: int):
        """Get Movie by id"""
        try:
            return MoviesService(db.session).get_item_by_id(movie_id)
        except ItemNotFound:
            abort(404, message="Movie not found")
