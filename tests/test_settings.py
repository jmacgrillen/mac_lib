#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        test_settings.py
    Desscription:
        Test the settings file.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import pytest
from unittest.mock import mock_open, patch
from maclib.mac_settings import MacSettings, MacSettingsException
import maclib.mac_file_management as file_man


fake_files = ["mysettings.yaml", "defaults.yaml"]

settings_dict = dict()
settings_dict['fake_load'] = True
settings_dict['something'] = dict()
settings_dict['something']['else'] = 'here'


def test_01_settings_default_exist(monkeypatch):
    """
    Test the logic works when the settings files exist

    Args:
        monkeypatch (_type_): _description_
    """
    global fake_files

    def mock_exists(os_path):
        """
        Make sure the file name passed is known about  and
        return true.

        Args:
            faked_name (str): File Name to check
        """
        assert os_path in fake_files
        return True

    monkeypatch.setattr(file_man, "does_exist", mock_exists)
    test_settings = MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])
    assert test_settings.settings_file_path == fake_files[0]
    assert test_settings.default_settings_path == fake_files[1]


def test_02_defaults_not_exist():
    """
    Test the logic works when the settings files exist

    Args:
        monkeypatch (_type_): _description_
    """
    global fake_files

    with pytest.raises(MacSettingsException):
        assert MacSettings(
           settings_file_path=fake_files[0],
           default_settings_path=fake_files[1])


def test_03_settings_not_exist(monkeypatch):
    """
    Test the logic works when the settings file does not exist

    Args:
        monkeypatch (_type_): _description_
    """
    global fake_files

    def mock_exists(os_path):
        """
        Make sure the file name passed is known about  and
        return true.

        Args:
            faked_name (str): File Name to check
        """
        if os_path == fake_files[0]:
            return False
        return True

    def copy_file(self):
        """
        Fake the file copy
        """
        pass

    monkeypatch.setattr(file_man, "does_exist", mock_exists)
    monkeypatch.setattr(MacSettings,
                        "_copy_default_settings",
                        copy_file)
    MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])


def test_04_load_settings(monkeypatch):
    """
    Test the load settings function works

    Args:
        monkeypatch (_type_): _description_
    """
    global fake_files
    global settings_dict

    def mock_exists(os_path):
        """
        Make sure the file name passed is known about  and
        return true.

        Args:
            faked_name (str): File Name to check
        """
        assert os_path in fake_files
        return True

    monkeypatch.setattr(file_man, "does_exist", mock_exists)

    test_settings = MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])

    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    assert test_settings.settings_file_path == fake_files[0]
    assert test_settings.default_settings_path == fake_files[1]
    assert test_settings.get_all_settings() == settings_dict


def test_05_load_failure(monkeypatch):
    """
    Test the load settings function works

    Args:
        monkeypatch (_type_): _description_
    """
    global fake_files
    global settings_dict

    str_yaml = "test: makeup\n"\
               "- function1:\n"\
               "    Stuff"

    def mock_exists(os_path):
        """
        Make sure the file name passed is known about  and
        return true.

        Args:
            faked_name (str): File Name to check
        """
        assert os_path in fake_files
        return True

    monkeypatch.setattr(file_man, "does_exist", mock_exists)

    test_settings = MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])

    with patch("builtins.open", mock_open(read_data=str_yaml)):
        with pytest.raises(MacSettingsException):
            assert test_settings.load_settings()


if __name__ == "__main__":  # pragma: no cover
    pass
