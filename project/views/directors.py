from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services import DirectorsService
from project.setup_db import db

directors_ns = Namespace("directors")


@directors_ns.route("/")
class DirectorsView(Resource):
    @directors_ns.response(200, "OK")
    def get(self):
        """Get all directors"""

        all_directors = DirectorsService(db.session).get_all_directors()

# TODO: think about using paginate somehow?
        # if request.values.get("page"):
        #     page = int(request.values.get("page"))
        #     all_directors = DirectorsService(db.session).paginate(page=page, per_page=12)

        if request.values.get("page"):
            page = int(request.values.get("page"))
            all_directors = all_directors[12 * (page - 1): 12 * page]

        return all_directors


@directors_ns.route("/<int:director_id>")
class DirectorView(Resource):
    @directors_ns.response(200, "OK")
    @directors_ns.response(404, "Director not found")
    def get(self, director_id: int):
        """Get director by id"""
        try:
            return DirectorsService(db.session).get_item_by_id(director_id)
        except ItemNotFound:
            abort(404, message="Director not found")
