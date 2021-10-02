#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_single.py
    Desscription:
        Singleton pattern instance class.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""


class MacSingleInstance(type):
    """
    This class is following the Singleton pattern, a class that
    is a single instance that persists across all modules no matter
    how many times the program calls for a new instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                MacSingleInstance, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


if __name__ == "__main__":
    pass
