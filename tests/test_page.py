import pytest

from algebra import Algebra
alg = Algebra()

from page import Page
pgs_0 = Page(id=1, title='Mars', header='Can Mars hospit life?', author='Pino', body='Yes.')
pgs_1 = Page()


class TestAlgebra:

    @staticmethod
    def test_sum():
        assert alg.sum(1, 3) == 4
        assert alg.sum(3, 1) == alg.sum(1, 3)
    @staticmethod
    def test_sub():
        assert alg.sub(2, 2) == 0
        assert alg.sub(2,3) == None
    @staticmethod
    def test_mul():
        assert alg.mul(1, 0) == 0

class TestAPI:

    @staticmethod
    def test_response():
        assert pgs_0._id == 1
        assert pgs_1._id == None
        assert pgs_0._page
        assert pgs_1._page 
        assert len(pgs_0._page.keys()) == 5
        assert len(pgs_1._page.keys()) == 5






