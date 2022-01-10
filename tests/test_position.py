from uff.position import Position
import unittest


class TestPosition:
    def test_position_instantiation(self):
        p1 = Position(1, 2, 3)

    def test_position_compare(self):
        p1 = Position(1, 2, 3)
        p2 = Position(1, 2, 3)
        assert p1 == p2

    def test_position_itterator(self):
        p1 = Position(1, 2, 3)
        p1_iter = iter(p1)

        assert 1 == next(p1_iter)
        assert 2 == next(p1_iter)
        assert 3 == next(p1_iter)
        with unittest.TestCase.assertRaises(self, StopIteration):
            next(p1_iter)
