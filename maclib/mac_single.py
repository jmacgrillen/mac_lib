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
from typing import Type, Any


class MacSingleInstance(type):
    """
    This metaclass implements the Singleton pattern, ensuring that
    only one instance of a class derived from it persists across all modules,
    regardless of how many times the program attempts to create a new instance.

    Instances are stored in a WeakValueDictionary to allow for proper
    garbage collection when the singleton instance is no longer strongly
    referenced elsewhere.
    """
    _instances: WeakValueDictionary[Type[Any], Any] = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        """
        Creates a new instance of the class if one does not already exist.
        If an instance already exists, the existing instance is returned.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls):
        """
        Removes the stored singleton instance for this class.

        The next attempt to instantiate the class will create a new singleton
        instance.
        """
        try:
            del cls._instances[cls]
        except KeyError:
            pass


if __name__ == "__main__":  # pragma: no cover
    pass
