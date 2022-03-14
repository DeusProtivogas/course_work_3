import datetime
import hashlib
import hmac
import calendar

from flask import request
from flask_restx import abort
from project.services import UsersService
from project.setup_db import db

from project.config import BaseConfig

import jwt

def get_tokens(user_data):

    email = user_data.get("email")
    password = user_data.get("password")

    if email and password:

        user = UsersService(db.session).get_pure_item_by_email(email)
        if user:
            password_hash = user.password


            if compare_password(password_hash, password):
                user_data = {"email": email, "password": password}
                return generate_tokens(user_data)
    return False

def generate_tokens(data):


    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)

    return {
        "access_token": access_token.decode("utf-8"),
        "refresh_token": refresh_token.decode("utf-8")
    }

def compare_password(pass_hash, password) -> bool:
    return hmac.compare_digest(
        pass_hash,
        hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("UTF-8"),
            BaseConfig.PWD_HASH_SALT,
            BaseConfig.PWD_HASH_ITERATIONS
        )
    )


def jwt_decode(token):
    try:
        decoded = jwt.decode(token, BaseConfig.SECRET_KEY, BaseConfig.JWT_ALGORITHM)

    except:
        return False
    else:
        return decoded

def get_refresh_tokens(user_data):
    refresh_token = user_data.get("refresh_token")
    data = jwt_decode(refresh_token)
    if data:
        tokens = get_tokens(data)
        return tokens
    return False

def auth_check():
    if "Authorization" not in request.headers:
        return False
    token = request.headers["Authorization"].split("Bearer ")[-1]
    return jwt_decode(token)

def auth_required(func):
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, "Authorization required")
    return wrapper

def get_user_id(user_tokens):

    access_token = user_tokens.get("Authorization").split("Bearer ")[-1]
    data = jwt_decode(access_token)
    print(data)
    if data:
        print(data)
        user_id = data.get("email")

        # user = UsersService(db.session).get_pure_item_by_id(user_id)

        # tokens = get_tokens(data)
        return user_id