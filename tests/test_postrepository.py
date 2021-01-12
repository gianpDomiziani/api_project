#TO DO: for now the correct way to execute these tests is: 
# 1) in the root directory run -> flask init-db
# 2) inside the tests directory run -> pytest test_postrepository.py

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
from uuid import uuid4

db_path = '../instance/app.sqlite'
#emptypost = post_model.Post(author_id=12).post
user1 = str(uuid4())
user2 = str(uuid4())
class TestRepositoryLayer:
    @staticmethod
    def test_repo_get_all():
        with dbhandler(db_path) as session:
            repo = post_repository.SQLiteRepository(session)
            posts = repo.get_all()
            cursor = session.cursor()
            expected = cursor.execute("SELECT p.id, title, body, username, created, author_id"
                             " FROM post p JOIN user u ON p.author_id = u.id"
                             " ORDER BY created DESC").fetchall()
        assert expected == posts, 'Returning posts should match all the posts present in DB.'

    @staticmethod
    def test_repo_can_add_post():
        # add a fake user
        with dbhandler(db_path) as session:
            cur = session.cursor()
            cur.execute("insert into user (username, password) values(?, ?)", (user1,'fakepwd'))
            cur.execute("insert into user (username, password) values(?, ?)", (user2,'fakepwd'))
            session.commit()
        
        false_id = 829
        true_id = 1
        true_post = post_model.Post().new_post(true_id,'New Title', 'New Body')
        false_post = post_model.Post().new_post(false_id,'New titleFALSE', 'New BodyFALSE')
        with dbhandler(db_path) as session:
            repo = post_repository.SQLiteRepository(session)
            err1 = repo.insert(true_post)
            err2 = repo.insert(false_post)
            session.commit()
            cursor = session.cursor()
            expected_true = cursor.execute(""" SELECT * FROM post WHERE author_id=? """, (true_id, )).fetchone()
            expected_false = cursor.execute(""" SELECT * FROM post WHERE author_id=? """, (false_id, )).fetchone()
        
        assert err1 == None
        assert err2 is not None
        assert expected_true[3] == 'New Title', 'Repo should add a new post with its correct title.'
        assert expected_false is None, 'Repo should add only post associated with a registered user.'
    
    @staticmethod
    def test_repo_get_post_by_id():
        id = 1
        with dbhandler(db_path) as session:
            repo = post_repository.SQLiteRepository(session)
            post = repo.get_post_by_id(id)
            post1 = repo.get_post_by_id('NAN')
        assert len(post) == 6, 'get_post_by_id should return a single Post dict coming from a Post object with 6 attributes (keys).'
        assert post1 is None, 'id should be a int && id should be present in DB.'
    
    @staticmethod
    def test_repo_get_posts_by_username():
        with dbhandler(db_path) as session:
            cur = session.cursor()
            repo = post_repository.SQLiteRepository(session)
            posts = repo.get_posts_by_username(user1)
            no_posts = repo.get_posts_by_username(user2)
        assert not no_posts 
        assert len(posts) == 1


    @staticmethod
    def test_repo_can_update():
        up = {'title': 'updated title', 'body': 'updated body'}
        true_author_id = 1
        true_post_id = 1
        false_author_id = 58
        false_post_id = 58
        with dbhandler(db_path) as session:
            repo = post_repository.SQLiteRepository(session)
            state_true = repo.update(true_author_id, true_post_id, up)
            state_false = repo.update(false_author_id, false_post_id, up)
            session.commit()
            updated_post = repo.get_post_by_id(true_post_id)
        assert state_true == True, 'Repo update should update a saved post.'
        assert state_false == False, 'Repo should not update a not present post.'
        assert updated_post['title'] == up['title']
        assert updated_post['body'] == up['body']
    
    
    @staticmethod
    def test_repo_can_delete():
        with dbhandler(db_path) as session:
            true_post_id = 1
            false_post_id = 78
            true_author_id = 1
            repo = post_repository.SQLiteRepository(session)
            false_status = repo.delete(true_author_id, false_post_id)
            true_status = repo.delete(true_author_id, true_post_id)
            session.commit()
            changes = session.total_changes
            cur = session.cursor()

        assert not false_status
        assert true_status
        assert changes == 1
