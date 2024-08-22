from flask import jsonify

from .exceptions import NotFoundException, UnauthorizedException, InvalidTokenError


def handle_not_found_exception(e):
    return jsonify({'message': str(e)}), 404


def handle_unauthorized_exception(e):
    return jsonify({'message': str(e)}), 401


def handle_invalid_token_error(e):
    return jsonify({'error': str(e)}), 401


def initialize_error_handlers(app):
    app.register_error_handler(NotFoundException, handle_not_found_exception)
    app.register_error_handler(UnauthorizedException, handle_unauthorized_exception)
    app.register_error_handler(InvalidTokenError, handle_invalid_token_error)


