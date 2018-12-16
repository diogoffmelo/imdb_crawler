from __future__ import division

import math
import random

import pytest

from imdb.numeric import Vector, StatVector


def test_vector():
    v1 = Vector([1, 1, 1])
    v2 = Vector([2, 2, 2])

    assert tuple(v2) == tuple(2 * v1)
    assert tuple(v2) == tuple(v1 * 2)
    assert tuple(v2) == tuple(v1 + v1)
    assert tuple(v2) == tuple(1 + v1)
    assert tuple(v2-1) == tuple(v1)
    assert tuple(-1 + v2) == tuple(v1)
    assert tuple(1 - v2) == tuple(-v1)
    assert tuple(v2) == tuple(v1 + 1)
    assert tuple(-v1) == (-1, -1, -1)
    assert v1.dot(v1) == 3
    assert tuple(v1 * v1) == tuple(v1)
    assert tuple(abs(-v1)) == tuple(v1)

    v1 = Vector([1, 1, 2])
    assert tuple(v1.filter(lambda x: x < 2)) == (1, 1)


def test_statvector():
    v1 = StatVector([1, 1, 1])
    assert v1.mean() == 1
    assert v1.mean() == v1.max()
    assert v1.mean() == v1.min()
    assert v1.std() == 0

    v1 = StatVector([1, 1, 4])
    assert v1.mean() == 2
    assert v1.min() == 1
    assert v1.max() == 4
    assert v1.var() == 2
    assert v1.std() == math.sqrt(2)
    assert v1.nstd() == math.sqrt(3)

    assert v1.prob(lambda x: x == 4) == 1/3
    assert v1.cond_prob(lambda x: x == 4, lambda x: x > 3) == 1

    v1 = StatVector([1, 1, 2, 2])

    assert v1.prob(lambda x: x < 0) == 0
    assert v1.prob(lambda x: x > 0) == 1
    assert v1.prob(lambda x: x > 3) == 0
    assert v1.prob(lambda x: x < 3) == 1
    assert v1.prob(lambda x: x == 2) == 0.5
    assert v1.prob(lambda x: x == 1) == 0.5

    assert v1.cond_prob(lambda x: x == 1, lambda x: True) == v1.prob(lambda x: x == 1) # noqua
    assert v1.cond_prob(lambda x: x == 1, lambda x: x == 1) == 1
    assert v1.cond_prob(lambda x: x == 1, lambda x: x != 1) == 0

    v1 = StatVector(random.random() for _ in range(10000))

    assert v1.cond_prob(lambda x: x < 0.5, lambda x: True) == v1.prob(lambda x: x < 0.5) # noqua
    assert v1.cond_prob(lambda x: x < 0.5, lambda x: x < 0.5) == 1
    assert v1.cond_prob(lambda x: x < 0.5, lambda x: x >= 0.5) == 0