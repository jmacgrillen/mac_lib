#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_detect.py
    Desscription:
        Find out about the platform the program is running on
        to help with trouble shooting.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import platform


class MacDetect(object):
    """
    Gather some information about the platform we're running on.
    """
    os_name: str = None
    os_version: str = None
    architecture: str = None
    python_version: str = None
    python_compiler: str = None
    python_implementation: str = None

    def __init__(self):
        """
        Run through the platform and gather the info.
        """
        platform_info = platform.uname()
        self.os_name = platform_info[0]
        self.os_version = platform_info[3]
        self.architecture = platform_info[4]
        self.python_version = platform.python_version()
        self.python_compiler = platform.python_compiler()
        self.python_implementation = platform.python_implementation()
