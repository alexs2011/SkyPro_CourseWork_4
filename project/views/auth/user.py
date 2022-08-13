from flask import request
from flask_restx import Namespace, Resource, abort

from project.container import user_service
from project.setup.api.models import user

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        headers = request.headers
        ref_token = headers.environ.get('HTTP_AUTHORIZATION').split()[-1]
        usr = user_service.get_user_by_token(ref_token=ref_token)
        if not usr:
            abort(401)
        return usr, 200

    def patch(self):
        data = request.json
        headers = request.headers
        ref_token = headers.environ.get('HTTP_AUTHORIZATION').split()[-1]
        updated_user_id = user_service.update_user(data=data, ref_token=ref_token)
        if not updated_user_id:
            abort(401)
        return updated_user_id, 201


@api.route('/password/')
class UserChangePasswordView(Resource):
    def put(self):
        data = request.json
        headers = request.headers
        ref_token = headers.environ.get('HTTP_AUTHORIZATION').split()[-1]
        updated_tokens = user_service.update_password(data=data, ref_token=ref_token)
        if not updated_tokens:
            abort(401)
        return updated_tokens, 201
