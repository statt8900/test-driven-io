# Typing imports
import typing as typ

# External imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import os

# Internal Imports


db = SQLAlchemy()  # new


def create_app(script_info: typ.Any = None) -> Flask:
    # instantiate the app
    app = Flask(__name__)

    # set configuration
    CONFIG = os.getenv("APP_SETTINGS")
    app.config.from_object(CONFIG)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from .api.users import users_blueprint

    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx() -> typ.Dict[str, typ.Any]:
        return {"app": app, "db": db}

    return app
