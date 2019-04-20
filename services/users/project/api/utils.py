# Typing imports
import typing as typ
# External imports
from functools import wraps
from flask import request, jsonify
import sys
# Internal Imports
from project.api.models import User

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response_object = {
        'status': 'fail',
        'message': 'Provide a valid auth token.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(response_object), 403
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if isinstance(resp, str):
            response_object['message'] = resp
            return jsonify(response_object), 401
        user = User.query.filter_by(id=resp).first()
        if not user:
            return jsonify(response_object), 401
        if not user.active:
            response_object['message'] = 'Provide a valid auth token.'
            return jsonify(response_object),401
        return f(resp, *args, **kwargs)
    return decorated_function

def is_admin(user_id:int)->bool:
    user = User.query.filter_by(id = user_id).first()
    if user:
        return user.admin
    return False
