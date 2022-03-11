import datetime
import hashlib
import hmac
import calendar

from flask_restx import abort
from project.services import UsersService
from project.setup_db import db

from project.config import BaseConfig

import jwt

def get_tokens(user_data):

    print(user_data)
    email = user_data.get("email")
    password = user_data.get("password")
    print(f"{email}, {password}")

    if email and password:
        print("test2")

        user = UsersService(db.session).get_item_by_email(email)
        print(user)
        if user:
            password_hash = user.password

            print(f"Hash pass from db: {password_hash}")
            print(f"Given pass: {password}")

            if compare_password(password_hash, password):
                print("test1")
                user_data = {"email": email, "password": password}
                return generate_tokens(user_data)
            print("test2")
    return False

def generate_tokens(data):

    print(data)

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=BaseConfig.TOKEN_EXPIRE_MINUTES)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=BaseConfig.TOKEN_EXPIRE_DAYS)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, BaseConfig.SECRET_KEY, algorithm=BaseConfig.JWT_ALGORITHM)

    print(f"AT: {access_token}")

    print(f"RT: {refresh_token}")
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

# def get_refresh_tokens(refresh_token):
#     data = jwt.decode(jwt=refresh_token, key=BaseConfig.SECRET_KEY, algorithms=[BaseConfig.JWT_ALGORITHM] )



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
    print(data)
    if data:
        tokens = get_tokens(data)
        return tokens
    return False