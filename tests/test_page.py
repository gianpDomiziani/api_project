
import pytest
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

from models.page import Page
from services.pageService import ServePages
from repositories import repository


pgs_0 = Page(id=0, title='Mars', header='Can Mars hold life?',
             author='Pino', body='Yes.')
pgs_1 = Page(id=1)


servPages = ServePages()


class TestAPI:

    @staticmethod
    def test_page():
        assert pgs_0.id == 0
        assert pgs_1.id == 1
        assert isinstance(pgs_0.page, dict)
        assert len(pgs_0.page.keys()) == 5
        assert len(pgs_1.page.keys()) == 5
        assert type(pgs_0.page['body']) == str

    @staticmethod
    def test_pages_are_unique_by_id():
        pgs_a = Page(id=12, title='Luna')
        pgs_b = Page(id=13, title='Luna')
        assert pgs_a != pgs_b

    # === ServePages Tests ===

    @staticmethod
    def test_servePages_charge():
        assert servPages.totPages == 0
        servPages.charge(pgs_1.page)
        assert servPages.totPages == 1
        assert servPages.pages[pgs_1.page['id']]

    @staticmethod
    def test_servePages_get():
        servPages.charge(pgs_1.page)
        assert servPages.get(pgs_1.page['id']) != None
        assert servPages.get('Not an ID') == None

    @staticmethod
    def test_servePages_delete():
        assert servPages.delete('Not an ID') == False
        servPages.charge(pgs_1.page)
        assert servPages.delete(pgs_1.page['id'])

    @staticmethod
    def test_servePages_modify():

        assert servPages.modify(id='Not an ID', field='title') is False
        servPages.charge(pgs_1.page)
        assert servPages.modify(pgs_1.page['id'], 'title', 'Modified')
    

    # === Abstract Repository Tests ===

    @staticmethod
    def test_repository_can_add_pages(session):

        ServePages.charge(pgs_0.page)
        repo = repository.SqlAlchemyRepository(session)
        page = ServePages.get(pgs_0.id)
        repo.add(page)
        session.commit()

        row = list(session.execute(
            ""
        ))

