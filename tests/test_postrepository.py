import pytest
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)
from app.models import post_model
from app.repositories import post_repository
from db.db_utils import dbhandler

import sqlite3

#emptypost = post_model.Post(author_id=12).post

class TestRepositoryLayer:
    @staticmethod
    def test_repo_get_all():
        with dbhandler() as session:
            repo = post_repository.SQLiteRepository(session)
            posts = repo.get_all()
            cursor = session.cursor()
            expected = cursor.execute("SELECT p.id, title, body, created, author_id, username"
                             " FROM post p JOIN user u ON p.author_id = u.id"
                             " ORDER BY created DESC").fetchall()
        assert expected == posts, 'Returning posts should match all the posts present in DB.'

    @staticmethod
    def test_repo_can_add_post():
        p = post_model.Post(829, 'New title', 'New Body.').post
        with dbhandler() as session:
            repo = post_repository.SQLiteRepository(session)
            repo.insert(p)
            session.commit()
            id_ = p['author_id']
            cursor = session.cursor()
            expected = cursor.execute(""" SELECT * FROM post WHERE author_id=? """, (id_, )).fetchone()
        assert  expected[3] == p['title'], 'The Adding post should match the request page.'
    
    @staticmethod
    def test_repo_get_a_post():
        id = 829
        with dbhandler() as session:
            repo = post_repository.SQLiteRepository(session)
            post = repo.get_by_id(id)
            post1 = repo.get_by_id('NAN')
        assert post['title'] == 'New title'
        assert post1 == False, 'id should be a int && id should be present in DB.'
    
    @staticmethod
    def test_repo_can_update():
        up = {'title': 'updated title', 'body': 'updated body'}
        true_id = 1
        false_id = 58
        with dbhandler() as session:
            repo = post_repository.SQLiteRepository(session)
            state_true = repo.update(true_id, up)
            state_false = repo.update(false_id, up)
            session.commit()
            updated_post = repo.get_by_id(true_id)
        assert state_true == True, 'Repo update should update a saved post.'
        assert state_false == False, 'Repo should not update a not present post.'
        assert updated_post['title'] == up['title']
        assert updated_post['body'] == up['body']
    
    
    @staticmethod
    def test_repo_can_delete():
        with dbhandler() as session:
            repo = post_repository.SQLiteRepository(session)
            repo.delete(829)
            session.commit()
            cur = session.cursor()
            expected1 = cur.execute(" SELECT * FROM post WHERE author_id=?", (829,)).fetchone()
            status = repo.delete('kl')
        assert expected1 == None
        assert status == False, 'id should be a int && id should be present in DB.'