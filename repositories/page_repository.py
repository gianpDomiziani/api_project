import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

# The repository Layer interacts with the Domain Model.
from models.page_model import Page


class SQLiteRepository:
    
    # a DB session is passed in order to instance a repository object.
    def __init__(self, session):
        self.session = session
        self.cursor = session.cursor()

    def insert(self, page):
        # avoid SQL injection attack
        page_tuple = (page['id'], page['title'], page['header'], page['author'], page['body'])
        self.cursor.execute("INSERT INTO pages(ID, TITLE, HEADER, AUTHOR, BODY) VALUES(?,?,?,?,?)", page_tuple)
        return 200
    
    def get_all(self) -> []:
        self.cursor.execute("SELECT * FROM pages")
        return self.cursor.fetchall()
    
    def get_by_id(self, id: int) -> dict:
        self.cursor.execute("SELECT * FROM pages WHERE id=?", (id,))
        page = self.cursor.fetchone()
        return page

    def update(self, id: int, req: dict) -> dict:
        if req['body']:
            self.cursor.execute(""" UPDATE pages SET body=? WHERE id=? """, (req['body'], id))
        if req['header']:
            self.cursor.execute(""" UPDATE pages SET header=? WHERE id=? """, (req['header'], id))
    


        

    def delete(self, id: int):
        self.cursor.execute("DELETE FROM pages WHERE id=?", (id,))

