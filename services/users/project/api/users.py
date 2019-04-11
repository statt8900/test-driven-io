# Typing imports
import typing as typ

# External imports
from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

# Internal Imports
from project.api.models import User
from project import db

response_type = typ.Tuple[str, int]
users_blueprint = Blueprint("users", __name__, template_folder="./templates")


@users_blueprint.route("/", methods=("GET", "POST"))
def index() -> str:
    if request.method == "GET":
        users = User.query.all()
        return render_template("index.html", users=users)
    else:
        username = request.form["username"]
        email = request.form["email"]
        if username and email:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            users = User.query.all()
            return render_template("index.html", users=users)


@users_blueprint.route("/users/ping", methods=("GET",))
def ping_pong() -> str:
    return jsonify({"status": "success", "message": "pong!"})


@users_blueprint.route("/users", methods=("POST", "GET"))
def add_user() -> typ.Tuple[str, int]:
    if request.method == "POST":
        response_obj = {"status": "fail", "message": "Invalid payload"}
        post_data = request.get_json()
        if not post_data:
            return jsonify(response_obj), 400

        username = post_data.get("username")
        email = post_data.get("email")
        if not (username and email):
            return jsonify(response_obj), 400
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email))
                db.session.commit()
                response_obj["message"] = f"{email} was added!"
                response_obj["status"] = " success"
                return jsonify(response_obj), 201
            else:
                response_obj["message"] = f"{email} already in database"
                return jsonify(response_obj), 400
        except exc.IntegrityError:
            db.session.rollback()
            return jsonify(response_obj), 400
    else:
        response_obj = {
            "status": "success",
            "data": {"users": [user.to_json() for user in User.query.all()]},
        }
        return jsonify(response_obj), 200


@users_blueprint.route("/users/<user_id>", methods=("GET",))
def get_user(user_id: int) -> response_type:
    """get a user by their id in the user table"""
    response_obj = {"status": "fail", "message": "User does not exist"}
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_obj), 404
        else:
            response_obj = {
                "status": "success",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "active": user.active,
                },
            }
            return jsonify(response_obj), 200
    except ValueError:
        return jsonify(response_obj), 404
