import pytest

from page import Page, ServePages
pgs_0 = Page(id=1, title='Mars', header='Can Mars hold life?', author='Pino', body='Yes.')
pgs_1 = Page()

servPages = ServePages()

class TestAPI:

    @staticmethod
    def test_page():
        assert pgs_0._id == 1
        assert pgs_1._id == None
        assert pgs_0._page
        assert pgs_1._page 
        assert len(pgs_0._page.keys()) == 5
        assert len(pgs_1._page.keys()) == 5
        assert type(pgs_0._page['body']) == str
        assert type(pgs_0._page) == dict
        assert type(pgs_1._page) == dict
    
    @staticmethod
    def test_pages_are_unique_by_id():
        pgs_a = Page(id=12, title='Luna')
        pgs_b = Page(id=13, title='Luna')
        assert pgs_a != pgs_b

    # === ServePages Tests ===
    
    @staticmethod
    def test_servePages_charge():
        servPages.charge(pgs_1._page)
        assert servPages._pages[pgs_1._page['id']]
    
    @staticmethod
    def test_servePages_get():
        servPages.charge(pgs_1._page)
        assert servPages.get(pgs_1._page['id']) != None
        assert servPages.get('Not an ID') == None
    
    @staticmethod
    def test_servePages_delete():
        assert servPages.delete('Not an ID') == False
        servPages.charge(pgs_1._page)
        assert servPages.delete(pgs_1._page['id'])

    @staticmethod
    def test_servePages_modify():

        assert servPages.modify(id='Not an ID', field='title') is False
        servPages.charge(pgs_1._page)
        assert servPages.modify(pgs_1._page['id'], 'title', 'Modified')