import pytest
import sqlite3
from uuid import uuid4

import init_path

from db.db_utils import dbhandler

from app.repositories import auth_repository

fake_user = {'username': 'fake_usr', 'password': 'fake_psw'}
true_user = {'username': 'Gianni', 'password': '1234'}

class TestAuthRepo:

    @staticmethod
    def test_get_user():
        with dbhandler() as session:
            repo = auth_repository.SQLiteRepository(session)
            cur = session.cursor()

            fake_usr = repo.get_user(fake_user['username'])
            expected_fake = cur.execute("SELECT * FROM user WHERE username=?", (fake_user['username'],)).fetchone()

            true_usr = repo.get_user(true_user['username'])
            expected_true = cur.execute("SELECT * FROM user WHERE username=?", (true_user['username'],)).fetchone()

        assert expected_fake == fake_usr
        assert tuple(expected_true) == tuple(true_usr)
        assert fake_usr == None, 'Login requires a valid username.'
    
    @staticmethod
    def test_get_id_from_user():
        
        true_username = 'Gianni'
        false_username = 'NAN'
        with dbhandler() as session:
            repo = auth_repository.SQLiteRepository(session)
            cur = session.cursor()
            true_usr_id = repo.get_id_from_user(true_username)
            false_usr_id = repo.get_id_from_user(false_username)
            expected = cur.execute("SELECT * FROM user WHERE username=?", (true_username,)).fetchone()
        assert true_usr_id, 'get_id_from_user should return an integer for valid id.'
        assert true_usr_id == expected[0], 'get_id_from_user should return a correct user id for valid id.'
        assert false_usr_id is None, "get_id_from_user should return a non-value for invalid id."
    
    @staticmethod
    def test_get_user_from_id():
        
        true_id = 1
        false_id = 'NAN'
        with dbhandler() as session:
            repo = auth_repository.SQLiteRepository(session)
            cur = session.cursor()

            true_usr = repo.get_user_from_id(true_id)
            false_usr = repo.get_user_from_id(false_id)

            expected = cur.execute("SELECT * FROM user WHERE id=?", (true_id,)).fetchone()
        
        assert true_usr, "get_user_from_id should return a value for valid id."
        assert tuple(true_usr) == (expected[0], expected[1]), 'get_user_from_id should return a correct user for valid username.'
        assert false_usr is None, 'get_user_from_id should return a none value for invalid id.'

    @staticmethod
    def test_new_user():
        new_user = {'username': f'test{str(uuid4())}', 'password': 'test1'}
        with dbhandler() as session:
            repo = auth_repository.SQLiteRepository(session)
            cur = session.cursor()
            repo.new_user(new_user['username'], new_user['password'])
            session.commit()

            expected = cur.execute("SELECT * FROM user WHERE username=?", (new_user['username'],)).fetchone() 

        assert expected, 'new_user should add a new user.'
        assert expected[1] == new_user['username'], 'new_user should add a new user with correct username.'   
        assert expected[2] == new_user['password'], 'new_user should add a new user with the correct password.'