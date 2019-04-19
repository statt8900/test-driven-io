# Typing imports
import typing as typ
# External imports
from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

# Internal Imports
from project.api.models import User
from project import db, bcrypt

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=('POST',))
def register_user() -> typ.Tuple[str, typ.Any]:
    response_obj = {
        'message': 'Invalid payload.',
        'status': 'fail'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_obj), 400

    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')

    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()

        if not user:
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_obj = {'status': 'success',
                            'message': 'Successfully registered.',
                            'auth_token': auth_token.decode()
                            }
            return jsonify(response_obj), 201
        else:
            response_obj['message'] = 'Sorry. That user already exists.'
            return jsonify(response_obj), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_obj['traceback'] = e.__repr__()
        return jsonify(response_obj), 400


@auth_blueprint.route('/auth/login', methods=('POST',))
def login_user() -> typ.Tuple[str, typ.Any]:
    response_obj = {
        'message': 'Invalid payload.',
        'status': 'fail'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_obj), 400

    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_obj['status'] = 'success'
                response_obj['message'] = 'Successfully logged in.'
                response_obj['auth_token'] = auth_token.decode()
                return jsonify(response_obj), 200
        else:
            response_obj['message'] = 'User does not exist.'
            return jsonify(response_obj), 404

    except Exception as e:
        print(e)
        response_obj['message'] = e.__repr__()
        return jsonify(response_obj), 500


@auth_blueprint.route('/auth/logout', methods=('POST',))
def logout_user() -> typ.Tuple[str, typ.Any]:
    response_object = {
        'message': 'Invalid payload.',
        'status': 'fail'
    }
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[-1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully logged out.'
            return jsonify(response_object), 200
        else:
            response_object['status'] = 'fail'
            response_object['message'] = resp
            return jsonify(response_object), 401
    else:
        return jsonify(response_object), 403


@auth_blueprint.route('/auth/status', methods=('GET',))
def get_status() -> typ.Tuple[str, typ.Any]:
    response_object = {
        'message': 'Invalid payload.',
        'status': 'fail'
    }
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(' ')[-1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            response_object['data'] = user.to_json()
            response_object['status'] = 'success'
            return jsonify(response_object), 200
        else:
            response_object['status'] = 'fail'
            response_object['message'] = resp
            return jsonify(response_object), 401
    else:
        return jsonify(response_object), 403
