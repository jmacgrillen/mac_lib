#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        test_detect.py
    Desscription:
        Test the system detection functions.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import platform
import winreg
import maclib.mac_detect as mdetect


def test_detect_01_test_platform_not_windows(monkeypatch):
    """
    Test that we're pulling back the right data
    """
    uname_list = [
            "macware",
            "filler",
            "filler",
            "2.0",
            "RISC III",
        ]

    def uname_data():
        """
        Mock out the data return.
        """
        return uname_list

    monkeypatch.setattr(platform, 'uname', uname_data)
    tested_detect = mdetect.MacDetect()
    assert tested_detect.os_name == uname_list[0]
    assert tested_detect.os_version == uname_list[3]
    assert tested_detect.architecture == uname_list[4]
    assert 'os_theme' not in vars(tested_detect)


def test_detect_02_test_platform_windows_dark(monkeypatch):
    """
    Test that we're pulling back the right data
    """
    key_value = "my_mocked_key"
    uname_list = [
            "Windows",
            "filler",
            "filler",
            "12.0",
            "RISC III",
        ]

    def uname_data():
        """
        Mock out the data return.
        """
        return uname_list

    def openkey_data(key: int, sub_key: str):
        """
        Mock out Winreg openkey
        """
        assert key == winreg.HKEY_CURRENT_USER
        assert sub_key == "Software\\Microsoft\\Windows\\" \
                          "CurrentVersion\\Themes\\Personalize"
        return key_value

    def query_value_output(key: str, subkey: str):
        """
        Lastly get the query_value mocked
        """
        assert key == key_value
        assert subkey == "AppsUseLightTheme"
        data_values = [
            0,
            1,
            2,
            3,
        ]
        return data_values

    monkeypatch.setattr(winreg, 'OpenKey', openkey_data)
    monkeypatch.setattr(winreg, 'QueryValueEx', query_value_output)
    monkeypatch.setattr(platform, 'uname', uname_data)
    tested_detect = mdetect.MacDetect()
    assert tested_detect.os_name == uname_list[0]
    assert tested_detect.os_version == uname_list[3]
    assert tested_detect.architecture == uname_list[4]
    assert tested_detect.os_theme == "Dark"


def test_detect_03_test_platform_windows_light(monkeypatch):
    """
    Test that we're pulling back the right data
    """
    key_value = "my_mocked_key"
    uname_list = [
            "Windows",
            "filler",
            "filler",
            "12.0",
            "RISC III",
        ]

    def uname_data():
        """
        Mock out the data return.
        """
        return uname_list

    def openkey_data(key: int, sub_key: str):
        """
        Mock out Winreg openkey
        """
        assert key == winreg.HKEY_CURRENT_USER
        assert sub_key == "Software\\Microsoft\\Windows\\" \
                          "CurrentVersion\\Themes\\Personalize"
        return key_value

    def query_value_output(key: str, subkey: str):
        """
        Lastly get the query_value mocked
        """
        assert key == key_value
        assert subkey == "AppsUseLightTheme"
        data_values = [
            1,
            1,
            2,
            3,
        ]
        return data_values

    monkeypatch.setattr(winreg, 'OpenKey', openkey_data)
    monkeypatch.setattr(winreg, 'QueryValueEx', query_value_output)
    monkeypatch.setattr(platform, 'uname', uname_data)
    tested_detect = mdetect.MacDetect()
    assert tested_detect.os_name == uname_list[0]
    assert tested_detect.os_version == uname_list[3]
    assert tested_detect.architecture == uname_list[4]
    assert tested_detect.os_theme == "Light"
