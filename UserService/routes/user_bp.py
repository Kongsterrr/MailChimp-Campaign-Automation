from flask import Blueprint
from ..controllers.user_controller import *



user_blueprint = Blueprint('users', __name__, url_prefix='/users')
# user_blueprint.add_url_rule('/<int:user_id>', view_func=UserView.as_view('user'), methods=['GET', 'PUT'])
user_blueprint.add_url_rule('/register', view_func=UserRegisterView.as_view('register_view'), methods=['POST'])
user_blueprint.add_url_rule('/authenticate', view_func=UserLoginView.as_view('login_view'), methods=['POST'])