#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_single.py
    Description:
        Singleton pattern instance class.
    Version:
        1 - Initial release
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

    Attributes:
        _instances (WeakValueDictionary):
            A dictionary of instances of the class.

    Methods:
        __call__:
            Create a new instance of the class if it does not exist. If it does
            exist, return the existing instance.
        clear:
            Remove the singleton.
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
