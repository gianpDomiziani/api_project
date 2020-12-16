import json
import logging
import logging.config
with open('../log_config.json', 'r') as f:
    log_config = json.load(f)
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

from flask_utils import *

from flask import (
    Blueprint, g, request, jsonify
)

bp = Blueprint('core_api', __name__, url_prefix='/api')

@bp.route('/locals')
def get_locals():

    try:
        logger.info("API.get_locals called ...")
        with open('../shared/data/Sicily_locals.json', 'r') as f:
            locals = json.loads(f.read())
        return build_json_response(locals, 200, 'API.get_locals' )
    except Exception as e:
        logger.error(f"API.get_locals error -> {e}")
        return build_error_response(str(e), api_method='API.get_locals')

@bp.route('/local/<int:id>')
def get_local(id):
    
    try:
        logger.info("API.get_local called ...")
        with open('../shared/data/Sicily_locals.json', 'r') as f:
            locals = json.loads(f.read())
        return build_json_response(locals[id], 200, 'API.get_local')
    except Exception as e:
        err = str(e)
        logger.error(f"API.get_local error -> {e}")
        return build_error_response(err, api_method='API.get_local')

    

    
