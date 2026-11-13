import flask
import os
import jwt
import datetime
from flask import request, make_response, jsonify
from . import db_session
from .users import User
from .errors import api_error
import uuid

blueprint = flask.Blueprint(
    'frod_api',
    __name__
)

config = os.getenv('RANDOM_SECRET')


def generate_token(id):
    payload = {
        'sub': str(id),
        'exp': datetime.datetime.now() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.now()
    }
    return jwt.encode(payload=payload, key=config, algorithm='HS256')


def create_user(json, data, outputtoken=True):
    j = json
    d = data
    path = "/api/v1/auth/register"
    try:
        details = []
        if "login" not in j.keys():
            details.append({
                "field": "fullName",
                "issue": 'must be',
                "rejectedValue": None
            })
        if "password" not in j.keys():
            details.append(details.append({
                "field": "password",
                "issue": 'must be',
                "rejectedValue": None
            }))
        if details:
            return api_error("VALIDATION_FAILED", "Некоторые поля не прошли валидацию", data, path, 422)
        user_password = j["password"]
        user_login = j["fullName"]
        details = []
        if len(user_login) < 2 or len(user_login) > 200:
            details.append({
                "field": "fullName",
                "issue": 'len must be >= 2 and <= 200',
                "rejectedValue": user_login
            })
        if len(user_password) < 8 or len(user_password) > 72:
            details.append({
                "field": "password",
                "issue": 'must be >= 8 and <= 72',
                "rejectedValue": "user_password"
            })
        r1 = 0
        r2 = 0
        for s in str(user_password):
            if r1 and r2:
                break
            if s.isalpha():
                r1 = 1
            if s in "0123456789":
                r2 = 1
        if r1 == 0 or r2 == 0:
            details.append({
                "field": "password",
                "issue": 'must nums and letters',
                "rejectedValue": "user_password"
            })
        if details:
            return api_error("VALIDATION_FAILED", "Некоторые поля не прошли валидацию", data, path, 422)
        user = User()
        user.login = user_login
        user.set_password(user_password)
        db_sess = db_session.create_session()
        users = []
        for x in db_sess.query(User):
            if x.login == user_login:
                users.append(x)
        if users:
            db_sess.close()
            return api_error("LOGIN_ALREADY_EXISTS", "Пользователь с таким логином уже существует", d, path, 409)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        if outputtoken:
            return make_response(jsonify({
                "accessToken": generate_token(user.id),
                "user": {
                    "id": f"{user.id}",
                    "login": user.login,
                    "createdAt": f"{d.date()}T{d.hour}:{d.minute}:{d.second}Z",
                    "updatedAt": f"{d.date()}T{d.hour}:{d.minute}:{d.second}Z"
                }
            }), 201)
        else:
            return make_response(jsonify({
                "id": f"{user.id}",
                "login": user.login,
                "createdAt": f"{d.date()}T{d.hour}:{d.minute}:{d.second}Z",
                "updatedAt": f"{d.date()}T{d.hour}:{d.minute}:{d.second}Z"
            }), 201)

    except Exception:
        return api_error("BAD_REQUEST", "Невалидный JSON", d, path, 400)


@blueprint.route('/api/v1/ping')
def ping():
    return make_response(jsonify({"status": "ok"}), 200)

@blueprint.route('/api/v1/auth/register', methods=['POST'])
def register():
    d = datetime.datetime.now()
    try:
        j = request.json
    except Exception:
        return api_error("BAD_REQUEST", "Невалидный JSON", d, "/api/v1/auth/register", 400)
    return create_user(j, d)