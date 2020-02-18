import converter as c
import pytest


def test_1():
    assert c._validate_amount(100) == 100


def test_2():
    assert True == False
