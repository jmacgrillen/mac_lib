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

from maclib.mac_exception import MacException
from typing import Any


class MacSingleInstance(object):
    """
    This class is following the Singleton pattern, a class that
    is a single instance that persists across all modules no matter
    how many times the program calls for a new instance.
    """
    __instance: object

    def __init__(self) -> None:
        super(MacSingleInstance, self).__init__()

    def __new__(cls, *args, **kwargs) -> Any:
        if not cls.__instance:
            cls.__instance = super(MacSingleInstance, cls).__new__(
                                cls, *args, **kwargs)
        return cls.__instance


class MacSingleDictionaryException(MacException):
    """
    Custom exception for the singleton dictionary
    """


class MacSingleDictionary(MacSingleInstance):
    """
    Build on the Singleton instance and add a dictionary.
    """

    data_dictionary: dict

    def __init__(self) -> None:
        super(MacSingleDictionary, self).__init__()

    def does_key_exist(self, key_name: str) -> bool:
        """
        Check whether the file contains the requested key.
        """
        if key_name in self.data_dictionary:
            return True
        return False

    def __setitem__(self, item_key: str, item_value: Any) -> None:
        """
        Update the stored item.
        """
        self.data_dictionary[item_key] = item_value

    def __getitem__(self, key: str) -> Any:
        """
        When requested return the value of a particular key.
        """
        if not self.data_dictionary:
            raise MacSingleDictionaryException(
                "The data dictionary is not available to query.")
        try:
            value = self.data_dictionary[key]
            return value
        except AttributeError as a_error:
            print(a_error)
            return None


if __name__ == "__main__":
    pass
