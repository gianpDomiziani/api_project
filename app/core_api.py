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
    return build_json_response(posts, 200, 'API.get_posts')

@bp.route('/post/<id>')
def get_post_by_id(id):
    db = get_db()
    repo = post_repository.SQLiteRepository(db)
    post = repo.get_post_by_id(id)
    if post:
        return build_json_response(post, 200, 'api.get_post_by_id')
    e = f"There is no post with id={id}"
    return build_error_response(e, 'api.get_post_by_id')

@bp.route('/posts/<username>')
def get_posts_by_username(username):
    db = get_db()
    repo = post_repository.SQLiteRepository(db)
    posts = repo.get_posts_by_username(username)
    if posts:
        return build_json_response(posts, 200, 'API.get_post_by_id')
    e = f'There are no posts for the username {username}.'
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
        logger.error(f"{log_index} data without title -> {json_post}")
        error = "No title."
    elif not json_post['body']:
        logger.error(f"{log_index} data without body -> {json_post}")
        error = "No body."
    if not error:
        db = get_db()
        repo = post_repository.SQLiteRepository(db)
        author_id = g.user[0]
        username = g.user[1]
        logger.debug(f"{log_index} -> author_id: {g.user[0]}, username: {g.user[1]}")
        new_post = post_model.Post().new_post(author_id=author_id, title=json_post['title'], body=json_post['body'])
        logger.debug(f'{log_index} new_post -> {new_post}')
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
        author_id = g.user[0]
        state = repo.update(author_id, id, json_update)
        if state:
            db.commit()
            changes = db.total_changes
            if changes > 0:
                return build_json_response('OK', 200, 'update')
            return build_error_response(f"{g.user[1]} can't modify the post {id}", 'update')
        else:
            return build_error_response(f'There are no post {id}.', 'update')
    e = 'No data in request.'   
    return build_error_response(e, 'update')
    
    
@bp.route('/delete/<id>')
@login_required
def delete(id):
    log_index = 'Core_api.delete>'
    db = get_db()
    repo = post_repository.SQLiteRepository(db)
    author_id = g.user[0]
    status = repo.delete(author_id, id)
    db.commit()
    changes = db.total_changes
    if status:
        if changes > 0:
            return build_json_response(f'page with id={id} removed', 200, 'delete')
        return build_error_response(f"{g.user[1]} can't delete post {id}", 'delete')
    return build_error_response(f"Post with id={id} is not present.", 'delete')

    