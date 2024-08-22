from flask import jsonify, request
from flask.views import MethodView

from ..services.user_services import UserService

class UserRegisterView(MethodView):
    def __init__(self):
        self.user_service = UserService()

    def post(self):
        user_data = request.get_json()
        success, message, user_id = self.user_service.create_user(user_data)
        if success:
            return jsonify({'message': message, 'user_id': user_id}), 201
        else:
            return jsonify({'message': message, 'user_id': user_id}), 400


class UserLoginView(MethodView):
    def __init__(self):
        self.user_service = UserService()

    def post(self):
        data = request.get_json()
        user_id, user_status = self.user_service.authenticate_user(data['email'], data['password'])

        if user_id:
            return jsonify({'Authentication status': 'Success', 'user_id': user_id, 'user_status': user_status}), 200

        return jsonify({'Authentication status': 'Failure'}), 401