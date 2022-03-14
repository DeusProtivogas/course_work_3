from flask import request, jsonify
from flask_restx import abort, Namespace, Resource

from project.exceptions import ItemNotFound
from project.services import UsersService
from project.services.auth_service import get_user_id
from project.schemas.user import UserSchema
from project.services.auth_service import compare_password, auth_required
from project.setup_db import db



users_ns = Namespace("user")

@users_ns.route("/")
class UserJSONDataView(Resource):
    @auth_required
    def get(self):
        data = request.headers

        user_email = get_user_id(data)

        user = UsersService(db.session).get_item_by_email(user_email)
        return jsonify(user)

    @auth_required
    def patch(self):
        data = request.json

        user_token = request.headers
        user_email = get_user_id(user_token)


        if "user_email" not in data:
            data["email"] = user_email


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

