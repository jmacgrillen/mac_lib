#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
from weakref import WeakValueDictionary


class MacSingleInstance(type):
    """
    This class is following the Singleton pattern, a class that
    is a single instance that persists across all modules no matter
    how many times the program calls for a new instance.
    """
    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = cls._instances[cls] = super(
                MacSingleInstance, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def clear(cls):
        """
        Remove the singleton
        """
        try:
            del cls._instances[cls]
        except KeyError:
            pass


if __name__ == "__main__":  # pragma: no cover
    pass
