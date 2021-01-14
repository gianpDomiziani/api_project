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
        posts_ = self._cursor.execute("SELECT p.id, author_id, username, title, body, created"
                             " FROM post p JOIN user u ON p.author_id = u.id"
                             " ORDER BY created DESC").fetchall()

        posts_ls = [Post(id_=p[0], author_id=p[1], author=p[2], 
                     title=p[3], body=p[4], created=str(p[5])).post for p in posts_]
        return posts_ls
    
    def get_post_by_id(self, id):
        post_ = self._cursor.execute("""
        SELECT p.id, author_id, username, title, body, created FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = ?
        """, (id,)).fetchone()
        if post_:
            post = Post(id_=post_[0], author_id=post_[1], author=post_[2], 
                     title=post_[3], body=post_[4], created=str(post_[5])).post
            return post
        return None
    
    def get_posts_by_username(self, username: str) -> []:
        posts_ = self._cursor.execute(
            """ SELECT p.id, author_id, username, title, body, created FROM post p JOIN user u ON p.author_id = u.id WHERE u.username=?""", (username,)
        ).fetchall()
        if posts_:
            posts = [Post(id_=p[0], author_id=p[1], author=p[2], 
                     title=p[3], body=p[4], created=str(p[5])).post for p in posts_]
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
            return str(e)

    
    def update(self, author_id: int, id: int, req: dict):
        """ UPDATE: update a post if the request comes from the owner of the post to be modified.
        author_id: int -> the identified of the request user;
        id: int -> post id to be modified.
        req: dict -> The title and/or body with the modified contents.
         """
        
        post = self.get_post_by_id(id)
        if post:
            if req['body']:
                self._cursor.execute(""" 
                UPDATE post SET body=?, edit=? WHERE author_id=? AND id=? """, (req['body'], 1, author_id, id)
                )
            if req['title']:
                self._cursor.execute(""" 
                UPDATE post SET title=?, edit=? WHERE author_id=? AND id=? """, (req['title'], 1, author_id, id)
                )
            # the correctness of the request has been already verified in the service layer.
            return True 
        return False 
        
    def delete(self, author_id: int, id: int):
        post = self.get_post_by_id(id)
        if post:
            self._cursor.execute("DELETE FROM post WHERE id=? AND author_id=?", (id, author_id)).fetchone()
            return True
        return False
    