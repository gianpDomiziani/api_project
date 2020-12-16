import json
import logging
import logging.config
with open('../log_config.json', 'r') as f:
    log_config = json.load(f)
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)

from flask import (
    Blueprint, g, request, jsonify
)

bp = Blueprint('core_api', __name__, url_prefix='/api')

@bp.route('/locals')
def get_locals():
    with open('../shared/data/Sicily_locals.json', 'r') as f:
        locals = json.loads(f.read())
    return jsonify(locals)

@bp.route('/local/<int:id>')
def get_local(id):
    with open('../shared/data/Sicily_locals.json', 'r') as f:
        locals = json.loads(f.read())
    return locals[id]

    

    
