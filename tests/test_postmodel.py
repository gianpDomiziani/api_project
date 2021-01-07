import pytest
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )
)

from models import page_model

pgs_0 = page_model.Page(id=0, title='Mars', header='Can Mars hold life?',
             author='Pino', body='Yes.')
pgs_1 = page_model.Page(id=1)



class TestModel:

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
        pgs_a = page_model.Page(id=12, title='Luna')
        pgs_b = page_model.Page(id=13, title='Luna')
        assert pgs_a != pgs_b
