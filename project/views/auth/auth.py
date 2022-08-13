from flask import request
from flask_restx import Namespace, Resource, abort

from project.container import user_service

api = Namespace('auth')


@api.route('/register/')
class AuthRegisterView(Resource):
    def post(self):
        req_json = request.json
        if req_json.get('email') and req_json.get('password'):
            user_service.create_user(req_json)
            return "", 201
        return "Неполные данные регистрации.", 401


@api.route('/login/')
class AuthLoginView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("email")
        password = req_json.get("password")
        if not (username and password):
            abort(400)

        tokens = user_service.login_user(username, password)
        if not tokens:
            abort(401)
        return tokens, 200

    def put(self):
        req_json = request.json
        ref_token = req_json.get("refresh_token")
        if not ref_token:
            abort(400)

        tokens = user_service.update_user_session(ref_token)
        if not tokens:
            abort(401)
        return tokens, 200
