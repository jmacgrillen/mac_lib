#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_detect.py
    Description:
        Find out about the platform the program is running on
        to help with trouble shooting.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import platform
import sys
if 'nt' in sys.builtin_module_names:  # pragma: no cover
    import winreg
else:  # pragma: no cover
    import fake_winreg as winreg  # type: ignore


class MacDetect(object):
    """
    Gather some information about the platform we're running on.

    Attributes:
        os_name (str):
            The name of the operating system.
        os_version (str):
            The version of the operating system.
        os_theme (str):
            The theme the operating system is using.
        architecture (str):
            The architecture of the operating system.
        python_version (str):
            The version of python we're running.
        python_compiler (str):
            The compiler used to compile python.
        python_implementation (str):
            The implementation of python we're running.

    Methods:
        __init__(self):
            Run through the platform and gather the info.
        detect_windows_theme(self) -> str:
            Check whether Windows is using dark mode or not.
    """
    os_name: str
    os_version: str
    os_theme: str
    architecture: str
    python_version: str
    python_compiler: str
    python_implementation: str

    def __init__(self):
        """
        Run through the platform and gather the info.

        Args:
            None
        """
        platform_info = platform.uname()
        self.os_name = platform_info[0]
        self.os_version = platform_info[3]
        self.architecture = platform_info[4]
        self.python_version = platform.python_version()
        self.python_compiler = platform.python_compiler()
        self.python_implementation = platform.python_implementation()
        if self.os_name == "Windows":
            self.detect_windows_theme()

    def detect_windows_theme(self) -> str:
        """
        Check whether Windows is using dark  mode or not.

        Args:
            None

        Return:
            str:
                The theme Windows is using.
        """
        key = winreg.OpenKey(key=winreg.HKEY_CURRENT_USER,
                             sub_key="Software\\Microsoft\\Windows\\"
                                     "CurrentVersion\\Themes\\Personalize")
        subkey = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
        if subkey == 0:
            self.os_theme = "Dark"
        else:
            self.os_theme = "Light"


if __name__ == "__main__":  # pragma: no cover
    pass
