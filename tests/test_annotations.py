from __future__ import annotations
from uff import TimeZeroReferencePoint


def test_annotations():
    assert TimeZeroReferencePoint.__annotations__ != {}, "Time zero reference point annotation dict is empty"
