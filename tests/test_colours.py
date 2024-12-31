#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        test_colours.py
    Desscription:
        Unit tests for mac_colours.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import maclib.mac_colours as colours


def test_limit_01_inrange():
    """
    Feed the function a number in the range 0-255 to
    make sure it works when fed with a number we expect.
    """
    test_number: int = 128
    assert colours.limit_number(test_number) == test_number


def test_limit_02_over_limit():
    """
    Test that if the number is over 255 it returns 255.
    """
    assert colours.limit_number(400) == 255


def test_limit_03_minus_number():
    """
    What happens if we use a minus number?
    """
    assert colours.limit_number(-10) == 0


def test_colour_01_inrange():
    """
    Test the return values align with what we think
    they should be.
    """
    expected_value = '#3ca184'
    assert colours.rgb2hex(red=60, green=161, blue=132) == expected_value


def test_colour_02_too_high():
    """
    Test what happens when one of the values is too high
    """
    expected_value = '#6effbd'
    assert colours.rgb2hex(red=110, green=500, blue=189) == expected_value


def test_colour_03_minus_number():
    """
    Test minus numbers return as a zero
    """
    expected_value = '#6e00bd'
    assert colours.rgb2hex(red=110, green=-50, blue=189) == expected_value


if __name__ == "__main__":
    pass
