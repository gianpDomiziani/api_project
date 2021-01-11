import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

from .custom_logger import logger

from app.flask_utils import *
from flask import (
    Blueprint, g, request, session
)


from app.repositories import post_repository
from app.models import post_model
from app.auth import login_required
from app.models import post_model
from app.db import get_db


bp = Blueprint('core_api', __name__, url_prefix='/api')

@bp.route('/posts')
def get_posts():
    log_index = 'Core_api.get_posts>'
    db = get_db()
    repo = post_repository.SQLiteRepository(db)
    posts = repo.get_all()
    logger.debug(f"posts: {posts}")
    posts_ls = [post_model.Post(p['author_id'], p['username'], p['title'], p['body']).post for p in posts]
    return build_json_response(posts_ls, 200, 'API.get_posts')

@bp.route('/posts/<username>')
def get_posts_by_username(username):
    db = get_db()
    repo = post_repository.SQLiteRepository(db)
    posts_ = repo.get_posts_by_username(username)
    if posts_:
        posts = [post_model.Post(post_['author_id'], post_['author'], post_['title'], post_['body']).post for post_ in posts_] 
        return build_json_response(posts, 200, 'API.get_post_by_id')
    e = 'Post is not present.'
    return build_error_response(e, 'API.get_post_by_id')

@bp.route('/insert', methods=['POST'])
@login_required
def insert():
    log_index = 'Core_api.insert>'
    json_post = request.get_json()
    error = None

    if not json_post:
        logger.error(f"{log_index} data must be in json format -> {json_post}")
        error = "data must be in json format."
    if not json_post['title']:
        error = "No title."
    elif not json_post['body']:
        error = "No body."
    if not error:
        db = get_db()
        repo = post_repository.SQLiteRepository(db)
        author_id = g.user[0]
        username = g.user[1]
        new_post = post_model.Post(author_id, username, json_post['title'], json_post['body']).post
        error = repo.insert(new_post)
        if error:
            return build_error_response(error, 'core_api.insert')
        db.commit()
        logger.info(f"{log_index} post: {new_post} insert")
        return build_json_response('OK', 200, 'insert')
    return build_error_response(error, 'core_api.insert')

@bp.route('/modify/<id>', methods=['POST'])
@login_required
def update(id):
    json_update = request.get_json()
    if 'title' or 'body' in json_update:
        db = get_db()
        repo = post_repository.SQLiteRepository(db)
        state = repo.update(id, json_update)
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
@login_required
def delete(id):
    log_index = 'Core_api.delete>'
    db = get_db()
    repo = post_repository.SQLiteRepository(db)
    status = repo.delete(id)
    db.commit()
    if status:
        return build_json_response(f'page with id={id} removed', 200, 'delete')
    return build_error_response(f'There is no page with id={id}', 'delete')

    