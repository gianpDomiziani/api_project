from models import page_model
from services import page_services
from repositories import page_repository
from test_pagemodel import pgs_0, pgs_1

servePages = page_services.ServePages()



class TestService:

    # === ServePages Tests ===

    @staticmethod
    def test_servePages_charge():
        assert servePages.totPages == 0
        servePages.charge(pgs_1.page)
        assert servePages.totPages == 1
        assert servePages.pages[pgs_1.page['id']]

    @staticmethod
    def test_servePages_get():
        servePages.charge(pgs_1.page)
        assert servePages.get(pgs_1.page['id']) != None
        assert servePages.get('Not an ID') == None

    @staticmethod
    def test_servePages_delete():
        assert servePages.delete('Not an ID') == False
        servePages.charge(pgs_1.page)
        assert servePages.delete(pgs_1.page['id'])

    @staticmethod
    def test_servePages_modify():

        assert servePages.modify(id='Not an ID', field='title') is False
        servePages.charge(pgs_1.page)
        assert servePages.modify(pgs_1.page['id'], 'title', 'Modified')
    

