import jwt
import datetime
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, make_response, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, set_access_cookies
import datetime
from functools import wraps


load_dotenv()

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except:
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

# Configure your Flask app and JWT
def authenticate(username, password, secure_username, secure_password):
    if username == secure_username and password == secure_password:
        # Create a JWT token
        access_token = create_access_token(identity=username)
        resp = make_response(redirect(url_for('home')))
        set_access_cookies(resp, access_token)
        return resp
    else:
        return False
