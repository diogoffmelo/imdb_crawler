import pytest

from imdb.numeric import Vector, StatVector


def test_vetor():
    v1 = Vector([1, 1, 1])
    v2 = Vector([2, 2, 2])

    assert True