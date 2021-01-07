import json
from flask import Flask, Response
#from app.custom_logger import logger
#from app.config import default_config, DevConfig

#
#def create_app():
#
#    logger.info("Application Factory> creating Flask app ...")
#    app = Flask(default_config['app_name'])
#    app.config.from_object(DevConfig)
#    logger.debug(f"app.config: {app.config}")
#
#    from . import core_api
#    logger.info("Registering blueprints ...")
#    app.register_blueprint(core_api.bp)
#
#    from app import db
#    db.init_app(app)
#
#    return app
#

def build_json_response(body: dict, http_status: int, api_method: str) -> Response:
        
        
        json_body = json.dumps(body, indent=4, sort_keys=False)
        response = Response(
            response = json_body,
            status = http_status,
            mimetype="application/json",
            headers = {"API method": api_method}
        )
        return response

def build_error_response(error: str, api_method: str) -> Response:

    return build_json_response(body={"error": [error]}, http_status=400, api_method=api_method)

