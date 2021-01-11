import pytest
import sqlite3

import init_path

from app.repositories import auth_repository

fake_user = {'username': 'fake_usr', 'password': 'fake_psw'}
true_user = {'username': 'Gianni', 'password': '1234'}

class TestAuthRepo:

    @staticmethod
    def test_get_user():
        session = sqlite3.connect('../istance/app.sqlite')
        cur = session.cursor()
        repo = auth_repository.SQLiteRepository(session)

        usr = repo.get_user(fake_user['username'])
        expected = cur.execute("SELECT * FROM user WHERE username=?", (fake_user['username'],))
        assert tuple(expected) == tuple(usr)
        assert usr == None