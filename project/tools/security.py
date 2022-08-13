import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import current_app

from project.config import config


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def compare_passwords(new_password: str, hashed_password):
    return hmac.compare_digest(
        hashed_password,
        generate_password_hash(new_password)
    )


def generate_tokens(user_dao, username, password, is_refresh=False):
    user = user_dao.get_user_by_login(username)
    if not user:
        return False

    if not is_refresh:
        is_password_valid = compare_passwords(password, user.password)
        if not is_password_valid:
            return False

    data = {
        "email": username,
    }

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data['exp'] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, config.JWT_SECRET, algorithm=config.JWT_ALGO)

    day30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    data['exp'] = calendar.timegm(day30.timetuple())
    refresh_token = jwt.encode(data, config.JWT_SECRET, algorithm=config.JWT_ALGO)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def approve_refresh_token(user_dao, refresh_token):
    try:
        data = jwt.decode(refresh_token, config.JWT_SECRET, algorithms=[config.JWT_ALGO])
    except Exception:
        return False
    username = data['email']

    user = user_dao.get_user_by_login(username)
    if not user:
        return False

    return generate_tokens(user_dao, username, user.password, is_refresh=True)


def get_data_from_token(refresh_token):
    try:
        data = jwt.decode(refresh_token, config.JWT_SECRET, algorithms=[config.JWT_ALGO])
    except Exception:
        return None

    return data
