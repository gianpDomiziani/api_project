import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

from models import page_model
from datetime import date

class TestOrm:

    @staticmethod
    def test_pages_mapper_can_load_pages(db_session):
        db_session.execute(
            """ INSERT INTO pages (title, header, author, body) 
            VALUES ('Marte is cool?', 'YEP', 'Pino', 'VERY GOOD.'),
                   ('Giove is cool?', 'YEP', 'Paolo', 'VERY NICE.'),
                   ('Saturno is cool?', 'NOPE', 'Marta', 'AWESOME.'), 
            """
        )
        expected = [
            page_model.Page("Marte is cool?", "YEP", "Pino", "VERY GOOD"),
            page_model.Page("Giove is cool?", "YEP", "Paolo", "VERY NICE"),
            page_model.Page("Saturno is cool?", "NOPE", "Marta", "AWESOME")
        ]
        assert db_session.query(page_model.Page).all() == expected
    
    @staticmethod
    def test_pages_mapper_can_save_page(db_session):
        new_page = page_model.Page('One title', 'One header', 'One author', 'One body')
        db_session.add(new_page)
        db_session.commit()

        rows = list(db_session.execute("SELECT title, header, author, body FROM pages"))
        assert rows == [('One title', 'One header', 'One author', 'One body')]

