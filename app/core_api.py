import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

# === Logger START===
import json
import logging
import logging.config
with open('../log_config.json', 'r') as f:
    log_config = json.load(f)
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
# === Logger END ===

from flask_utils import *
from flask import (
    Blueprint, g, request
)

import sqlite3

import config
from repositories import page_repository
from models import page_model
from db.db_utils import dbhandler

bp = Blueprint('core_api', __name__, url_prefix='/api')

@bp.route('/pages')
def get_pages():
    log_index = 'Core_api.get_pages>'
    with dbhandler() as session:
        repo = page_repository.SQLiteRepository(session)
        pages = repo.get_all()
        logger.info(f"{log_index} returning {pages}")
    return build_json_response(pages, 200, 'API.get_pages')

@bp.route('/page/<id>')
def get_page_by_id(id):
    with dbhandler() as session:
        repo = page_repository.SQLiteRepository(session)
        page = repo.get_by_id(id)
    if page:
        return build_json_response(page, 200, 'API.get_page_by_id')
    e = 'Page is not present.'
    return build_error_response(e, 'API.get_page_by_id')

@bp.route('/insert', methods=['POST'])
def insert():
    log_index = 'Core_api.insert>'
    json_page = request.get_json()
    if not json_page:
        logger.error(f"{log_index} data must be in json format -> {json_page}")
        error = "data must be in json format."
        return build_error_response(error, api_method='insert')
    with dbhandler() as session:
        repo = page_repository.SQLiteRepository(session)
        repo.insert(json_page)
        session.commit()
    logger.info(f"{log_index} page: {json_page} insert")
    return build_json_response('OK', 200, 'insert')

@bp.route('/modify/<id>', methods=['POST'])
def update(id):
    json_update = request.get_json()
    if 'body' or 'header' in json_update:
        with dbhandler() as session:
            repo = page_repository.SQLiteRepository(session)
            state = repo.update(id, json_update)
            session.commit()
        if state:
            return build_json_response('OK', 200, 'update')
        else:
            return build_error_response('Page is not present', 'update')
    e = 'No data in request.'   
    return build_error_response(e, 'update')
    
    
@bp.route('/delete/<id>')
def delete(id):
    log_index = 'Core_api.delete>'
    with dbhandler() as session:
        logger.debug(f'{log_index} id={id}')
        repo = page_repository.SQLiteRepository(session)
        status = repo.delete(id)
        session.commit()
    if status:
        return build_json_response(f'page with id={id} removed', 200, 'delete')
    return build_error_response(f'There is no page with id={id}', 'delete')

    