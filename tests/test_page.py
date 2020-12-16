import pytest

from page import Page
pgs_0 = Page(id=1, title='Mars', header='Can Mars hospit life?', author='Pino', body='Yes.')
pgs_1 = Page()

class TestAPI:

    @staticmethod
    def test_response():
        assert pgs_0._id == 1
        assert pgs_1._id == None
        assert pgs_0._page
        assert pgs_1._page 
        assert len(pgs_0._page.keys()) == 5
        assert len(pgs_1._page.keys()) == 5







