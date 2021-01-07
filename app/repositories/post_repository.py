import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

# The repository Layer interacts with the Domain Model.
from models.post_model import Post


class SQLiteRepository:
    
    # a DB session is passed in order to instance a repository object.
    def __init__(self, session):
        self._session = session
        self._cursor = session.cursor()

    def insert(self, new_post):
        # avoid SQL injection attack
        new_post = (new_post['author_id'], new_post['title'], new_post['body'])
        self._cursor.execute("INSERT INTO post(AUTHOR_ID, TITLE, BODY) VALUES(?,?,?)", new_post)
    
    def get_all(self) -> []:

        return self._cursor.execute("SELECT p.id, title, body, created, author_id, username"
                             " FROM post p JOIN user u ON p.author_id = u.id"
                             " ORDER BY created DESC").fetchall()
    
    def get_by_id(self, id: int) -> dict:
        self._cursor.execute("SELECT * FROM post WHERE author_id=?", (id,))
        post = self._cursor.fetchone()
        if post:
            return post
        return False

    def update(self, id: int, req: dict):
        post = self.get_by_id(id)
        if post:
            if req['body']:
                self._cursor.execute(""" UPDATE post SET body=?, edit=? WHERE author_id=? """, (req['body'], 1, id))
            if req['title']:
                self._cursor.execute(""" UPDATE post SET title=?, edit=? WHERE id=? """, (req['header'], 1, id))
            return True
        return False
    
    def delete(self, id: int):
        post = self.get_by_id(id)
        if post:
            self._cursor.execute("DELETE FROM post WHERE author_id=?", (id,))
            return True
        return False

