# Typing imports
import typing as typ

# External imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_debugtoolbar import DebugToolbarExtension  # type: ignore
from flask_cors import CORS  # type: ignore
import os

# Internal Imports
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
cors = CORS()

def create_app(script_info: typ.Any = None) -> Flask:
    # instantiate the app
    app = Flask(__name__)

    # set configuration
    CONFIG = os.getenv("APP_SETTINGS")
    app.config.from_object(CONFIG)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)

    # register blueprints
    from .api.users import users_blueprint

    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx() -> typ.Dict[str, typ.Any]:
        return {"app": app, "db": db}

    return app
