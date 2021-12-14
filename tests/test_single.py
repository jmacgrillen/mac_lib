#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        test_single.py
    Desscription:
        Unit tests for mac_single.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

from maclib.mac_single import MacSingleInstance


def test_single_01_instance_id():
    """
    Make sure that when we have 2 instances the IDs match
    """
    class TestClass(metaclass=MacSingleInstance):
        """
        Create a base test class
        """
        def __init__(self):
            """
            Initiate the class
            """
            super(TestClass, self).__init__()
            self.class_number = 1

    instance_one = TestClass()
    instance_two = TestClass()
    assert instance_one is instance_two


def test_single_02_shared_variable():
    """
    """
    class TestClass(metaclass=MacSingleInstance):
        """
        Create a base test class
        """
        class_number: int

        def __init__(self):
            """
            Initiate the class
            """
            super(TestClass, self).__init__()
            self.class_number = 0

    instance_one = TestClass()
    instance_two = TestClass()
    instance_one.class_number = 1
    instance_two.class_number = 2
    assert instance_two.class_number == instance_one.class_number


if __name__ == "__main__":
    pass
