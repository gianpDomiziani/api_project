from flask import Flask 
from .config import default_config, DevConfig
from . import repositories
from . import models


def create_app():

    app = Flask(default_config['app_name'])
    app.config.from_object(DevConfig())

    from app import core_api, auth
    app.register_blueprint(auth.bp)
    app.register_blueprint(core_api.bp)

    from app import db
    db.init_app(app)

    return app
