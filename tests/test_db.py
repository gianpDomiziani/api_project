import pytest

import init_path

from db.db_utils import dbhandler
db_path = '../instance/app.sqlite'
class TestDB:

    @staticmethod
    def test_db_foreign_key():
        with dbhandler(db_path) as session:
            cur = session.cursor()
            cur.execute("PRAGMA foreign_keys = 1")
            response = cur.execute("PRAGMA foreign_keys").fetchone()
        assert response == (1,)