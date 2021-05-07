from uff.position import Position


def test_position_instantiation():
    p1 = Position(1, 2, 3)


def test_position_compare():
    p1 = Position(1, 2, 3)
    p2 = Position(1, 2, 3)
    assert p1 == p2
