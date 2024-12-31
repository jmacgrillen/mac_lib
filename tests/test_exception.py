#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        test_exception.py
    Desscription:
        Test the custom Exception.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import maclib.mac_exception as mexception


def test_exception_01():
    """
    Test that the exception is raised properly
    """
    test_message = "Test exception"
    m_except = mexception.MacException(test_message)

    assert test_message in str(m_except)
