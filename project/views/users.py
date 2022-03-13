from flask import request
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services import UsersService
from project.schemas.user import UserSchema
from project.services.auth_service import compare_password, auth_required
from project.setup_db import db



users_ns = Namespace("user")

@users_ns.route("/all")
class UsersView(Resource):
    @auth_required
    def get(self):
        users = UsersService(db.session).get_all_users()

        return users


@users_ns.route("/")
class UserJSONDataView(Resource):
    @auth_required
    def get(self):
        data = request.json

        user = UsersService(db.session).get_item_by_id(data.get("id"))

        return user

    @auth_required
    def patch(self):
        data = request.json

        user = UsersService(db.session).update(data)
        return f"Updated: {user}"

@users_ns.route("/<int:user_id>")
class UserView(Resource):

    def get(self, user_id):
        user = UsersService(db.session).get_item_by_id(user_id)

        return user

    @auth_required
    def patch(self, user_id):
        data = request.json

        if "id" not in data:
            data["id"] = user_id

        user = UsersService(db.session).update(data)
        return f"Updated: {user}"

@users_ns.route("/password")
class PasswordChangeView(Resource):
    @auth_required
    def put(self):
        """
        password update
        """
        data = request.json
        user_id = int(data.get("id"))
        password1 = data.get("password1")
        password2 = data.get("password2")

        user = UsersService(db.session).get_pure_item_by_id(user_id)


        if compare_password(user.password, password1):
            user = UsersService(db.session).update_password(data)

        return f"Updated password: {user}"

