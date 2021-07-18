#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_colours.py
    Desscription:
        A small collection of colour conversion utilities.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""


def limit_number(num: int) -> int:
    """
    Limit the min and max of an int to a range of
    0 and 255.
    """
    return max(0, min(num, 255))


def rgb2hex(red: int, green: int, blue: int) -> str:
    """
    Convert RGB values to a hex string. i.e. #ffffff
    """
    return "#{0:02x}{1:02x}{2:02x}".format(
        limit_number(red),
        limit_number(green),
        limit_number(blue)
    )


if __name__ == "__main__":
    pass
