import pytest
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)
from models import page_model
from repositories import page_repository

import sqlite3

emptypage = page_model.Page(pageid=1).page

class TestRepositoryLayer:
    @staticmethod
    def test_repo_get_all():
        session = sqlite3.connect('../page.db')
        repo = page_repository.SQLiteRepository(session)
        pages = repo.get_all()
        cursor = session.cursor()
        expected = cursor.execute(""" SELECT * FROM pages """).fetchall()
        session.close()
        assert expected == pages, 'Returning pages should match all pages present in DB.'

    @staticmethod
    def test_repo_can_add_page():
        # TO DO: Note that the repository should interact with the DB and with the Domain model. 
        # This means the repo should get the page model structure from the page_model.
        p = {'id': 829, 'title': 'SQLite', 'header': 'with python', 'author': 'Gianni', 'body': 'OK'}
        #page = page_model.Page(p)
        session = sqlite3.connect('../page.db')
        repo = page_repository.SQLiteRepository(session)
        repo.insert(p)
        session.commit()
        id = p['id']
        cursor = session.cursor()
        expected = cursor.execute(""" SELECT * FROM pages WHERE id=? """, (id, )).fetchone()
        session.close()
        assert  expected[1] == p['title'], 'The Adding page should match the request page.'
    
    @staticmethod
    def test_repo_get_a_page():
        id = 829
        session = sqlite3.connect('../page.db')
        repo = page_repository.SQLiteRepository(session)
        page = repo.get_by_id(id)
        page1 = repo.get_by_id('NAN')
        session.close()
        assert page[1] == 'SQLite'
        assert page1 == False, 'id should be a int && id should be present in DB.'
    
    @staticmethod
    def test_repo_can_update():
        up = {'body': 'update body', 'header': 'update header'}
        session = sqlite3.connect('../page.db')
        repo = page_repository.SQLiteRepository(session)
        repo.update(829, up)
        session.commit()
        cur = session.cursor()
        expected = cur.execute(" SELECT * FROM pages WHERE id=?", (829,)).fetchone()
        status = repo.update('NAN', up)
        session.close()
        assert expected[4] == 'update body'
        assert expected[5] == 1
        assert status == False, 'id should be a int && id should be present in DB.'
    
    @staticmethod
    def test_repo_can_delete():
        session = sqlite3.connect('../page.db')
        repo = page_repository.SQLiteRepository(session)
        repo.delete(829)
        session.commit()
        cur = session.cursor()
        expected1 = cur.execute(" SELECT * FROM pages WHERE id=?", (829,)).fetchone()
        status = repo.delete('kl')
        session.close()
        assert expected1 == None
        assert status == False, 'id should be a int && id should be present in DB.'