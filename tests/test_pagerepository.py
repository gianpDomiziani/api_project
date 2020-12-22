import pytest
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)
from models import page_model
from orm import page_orm
from repositories import page_repository

class TestRepository:
    """ Integration test: we're testing if our repository interacts well with the DB. """

    @staticmethod
    def test_repo_can_save_a_page(session):

        page = page_model.Page()  # empty page
        repo = page_repository.SqlAlchemyRepository(session)
        repo.add(page)  # method under testing
        session.commit()

        rows = list(session.execute(
            """ SELECT pageid, title, header, author, body FROM pages """
        ))
        assert rows == [('', '', '', '', '')]


    def retrive_idpage(self, session):
        session.execute(
            """ INSERT INTO pages (pageid, title, header, author, body)
                VALUES (123, 'WOW', '?', 'Pino', 'Nothing')  """
        )
        [[page_id]] = session.execute(
            """ SELECT id FROM pages WHERE pageid=:123 AND title=:'WOW' """
        )
        return page_id

    def test_repo_can_load_a_page(self, session):
        
        page_id = self.retrive_idpage(session)
        repo = page_repository.SqlAlchemyRepository(session)
        retrived = repo.get(page_id)

        expected = page_model.Page(123, 'WOW', '?', 'Pino', 'Nothing')
        assert retrived.pageid == expected.pageid
        assert retrived.body == expected.body
    





