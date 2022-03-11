import hashlib

from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService

from project.config import BaseConfig # PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_SECRET, JWT_ALGORITHM


class UsersService(BaseService):
    def get_item_by_id(self, pk):

        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_item_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        print(user)
        return user
        # return UserSchema().dumps(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def create(self, user_data):
        password = user_data.get("password")

        if password:
            user_data["password"] = get_hash(password)

        return UserDAO(self._db_session).create(user_data)



def get_hash(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('UTF-8'),
        BaseConfig.PWD_HASH_SALT,
        BaseConfig.PWD_HASH_ITERATIONS
    )
