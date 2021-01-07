
from flask import Flask 
from app.custom_logger import logger
from app.config import default_config, DevConfig

def create_app():

    logger.info("Application Factory> creating Flask app ...")
    app = Flask(default_config['app_name'])
    app.config.from_object(DevConfig())
    #logger.debug(f"app.config: {app.config}")

    from app import core_api, auth
    logger.info("Registering blueprints ...")
    app.register_blueprint(auth.bp)
    app.register_blueprint(core_api.bp)

    from app import db
    db.init_app(app)

    return app