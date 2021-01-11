import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

import sqlite3
# The repository Layer interacts with the Domain Model.
from models.post_model import Post


class SQLiteRepository:
    
    # a DB session is passed in order to instance a repository object.
    def __init__(self, session):
        self._session = session
        self._cursor = session.cursor()
    
    def get_all(self):
        return self._cursor.execute("SELECT p.id, title, body, username, created, author_id"
                             " FROM post p JOIN user u ON p.author_id = u.id"
                             " ORDER BY created DESC").fetchall()
    
    def get_posts_by_id(self, author_id):
        posts = self._cursor.execute("""
        SELECT author_id, username, title, body FROM post p JOIN user u ON p.author_id = u.id WHERE p.author_id=?
        """, (author_id,)).fetchall()
        if posts:
            posts = [Post(author_id=post[0], author=post[1], title=post[2], body=post[3]).post for post in posts]
            return posts
        return None
    
    def get_posts_by_username(self, username: str) -> []:
        posts = self._cursor.execute(
            """ SELECT author_id, username, title, body FROM post p JOIN user u ON p.author_id = u.id WHERE u.username=?""", (username,)
        ).fetchall()
        if posts:
            posts = [Post(author_id=post[0], author=post[1], title=post[2], body=post[3]).post for post in posts]
            return posts
        return False

    def insert(self, post):
        author_id = post['author_id']
        title = post['title']
        body = post['body']
        self._cursor.execute("PRAGMA foreign_keys = 1")
        try:
            self._cursor.execute("insert into post (author_id, title, body) values(?,?,?)", (author_id, title, body))
            return None
        except sqlite3.IntegrityError as e:
            return e

    
    def update(self, id: int, req: dict):
        posts = self.get_posts_by_id(id)
        if posts:
            if req['body']:
                self._cursor.execute(""" UPDATE post SET body=?, edit=? WHERE author_id=? """, (req['body'], 1, id))
            if req['title']:
                self._cursor.execute(""" UPDATE post SET title=?, edit=? WHERE author_id=? """, (req['title'], 1, id))
            return True
        return False
    
    def delete(self, id: int):
        post = self.get_posts_by_id(id)
        if post:
            self._cursor.execute("DELETE FROM post WHERE id=?", (id,))
            return True
        return False
    


