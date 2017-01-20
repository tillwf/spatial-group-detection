# encoding: UTF-8

from nose.tools import *
from metrics import *


def test_haversine():
    X = (48.86699, 2.36022777)
    Y = (48.86690, 2.36022775)

    assert(round(haversine(X, Y), 3) == 0.01)
    assert(round(haversine(X, X), 3) == 0.0)


def test_haversine_acc():
    X = (48.86699, 2.36022777, 10)
    Y = (48.86690, 2.36022775, 10)
    print haversine_acc(X, Y)
    assert(round(haversine_acc(X, Y), 3) == 0.015)