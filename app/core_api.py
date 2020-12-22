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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from repositories import page_repository
from models import page_model
from services import page_services
from orm import page_orm

page_orm.start_mapper()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
session = get_session()
logger.debug(f"session bind: {session.bind}")

bp = Blueprint('core_api', __name__, url_prefix='/api')

@bp.route('/pages')
def get_pages():
    session = get_session()
    repo = page_repository.SqlAlchemyRepository(session)
    pages = repo.list()
    return build_json_response(pages, 200, 'API.get_pages')

@bp.route('/page/<int:id>')
def get_page_by_id(id):
    page = repo.get(id)
    return build_json_response(page, 200, 'API.get_page_by_id')

    

    
