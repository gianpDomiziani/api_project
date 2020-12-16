import pytest

from algebra import Algebra
alg = Algebra()



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




