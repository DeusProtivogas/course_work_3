import hashlib

from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
# from project.services.auth import get_user_id()

from project.config import BaseConfig # PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_SECRET, JWT_ALGORITHM


class UsersService(BaseService):
    def get_item_by_id(self, pk):
        """
        Get jsonified User object by id for output
        """
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema(only=("name", "surname", "email")).dump(user)


    def get_pure_item_by_id(self, pk):
        """
        Get User object by id for changes purposes (password included, but not shown)
        """
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return user

    def get_item_by_email(self, email):
        """
        Get jsonified User object by email for output
        """
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema(only=("name", "surname", "email")).dump(user)

    def get_pure_item_by_email(self, email):
        """
        Get User object by email for changes purposes (password included, but not shown)
        """
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return user

    def get_all_users(self):
        """
        Get all users
        """
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True, only=("name", "surname", "email")).dump(users)

    def create(self, user_data):
        """
        Creating a new user
        :param user_data: json object with necessary data
        :return:
        """
        password = user_data.get("password")

        if password:
            user_data["password"] = get_hash(password)
        user = UserDAO(self._db_session).create(user_data)
        return user #UserDAO(self._db_session).create(user_data)

    def update(self, user_data):
        return UserDAO(self._db_session).update(user_data)

    def update_password(self, user_data):

        password = user_data.get("password2")
        user_data["password2"] = get_hash(password)

        user = UserDAO(self._db_session).update_password(user_data)

        return user



def get_hash(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('UTF-8'),
        BaseConfig.PWD_HASH_SALT,
        BaseConfig.PWD_HASH_ITERATIONS
    )
