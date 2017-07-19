#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tspreprocess.skeleton import fib

__author__ = "Maximilian Christ"
__copyright__ = "Maximilian Christ"
__license__ = "none"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
