from flask import (
    g, Blueprint, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash
import functools

from .repositories import auth_repository
from .custom_logger import logger
from .flask_utils import *
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# login_required decorator to be used in core_api
def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if not g.user:
            return build_error_response('User is not logged in.', f'{view}')
        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """ Before serving any requests, check if an user is already logged. If yes store its information in g.user. """

    user_id = session.get('user_id')
    
    if not user_id:
        g.user = None
    else:
        db = get_db()
        repo = auth_repository.SQLiteRepository(db)
        user = repo.get_user_from_id(user_id)
        g.user = user


@bp.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == "POST":
        req_dict = request.get_json()
        username = req_dict['username']
        password = req_dict['password']
        db = get_db()
        repo = auth_repository.SQLiteRepository(db)
        user = repo.get_user(username)
        error = None

        if (not user) or (not check_password_hash(user['password'], password)):
            error = 'Username or Password not valid.'
            return build_error_response(error, 'auth.login')

        session.clear()
        session['user_id'] = user['id']
        msg = "User {0} logged.".format(user['id'])
        return build_json_response(msg, 200, 'auth.login')
         


@bp.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        req_dict = request.get_json()
        username = req_dict['username']
        password = req_dict['password']
        db = get_db()
        repo = auth_repository.SQLiteRepository(db)
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif repo.get_id_from_user(username) is not None:
            error = f"Username {username} is already registered."
        
        if not error:
            repo.new_user(username, generate_password_hash(password))
            db.commit()
            return build_json_response(f'Username {username} registered.', 200, 'auth.register')

        return build_error_response(error, 'auth.register')

@bp.route('/logout')
def logout():
    session.clear()