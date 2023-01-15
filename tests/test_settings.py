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
settings_dict['fake_load'] = 'True Dat'
settings_dict['something'] = dict()
settings_dict['something']['else'] = 'here'


def test_01_settings_default_exist(monkeypatch):
    """
    Test the logic works when all the settings files exist

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
    Test the logic works when the default settings file
    does not exist

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
    Test the load settings function handles YAML failures
    as expected

    Args:
        monkeypatch (_type_): _description_
    """
    global fake_files

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


def test_06_get_item(monkeypatch):
    """
    Test the __getitem__ function is working as expected

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

    # Patch in the does_exist
    monkeypatch.setattr(file_man, "does_exist", mock_exists)
    test_settings = MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    # The asserts will test the __getitem__ function
    assert test_settings['fake_load'] == settings_dict['fake_load']
    assert test_settings['something', 'else'] == settings_dict[
        'something']['else']


def test_07_get_item_fail(monkeypatch):
    """
    Test the __getitem__ function is working as expected

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

    # Patch in the does_exist
    monkeypatch.setattr(file_man, "does_exist", mock_exists)
    test_settings = MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    with pytest.raises(MacSettingsException):
        assert test_settings['not-there']


def test_08_save_file_normal(monkeypatch):
    """
    Test the save_settings function is working as expected

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

    # Patch in the does_exist
    monkeypatch.setattr(file_man, "does_exist", mock_exists)
    test_settings = MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    # Patch again,this time for the save operation
    with patch("builtins.open", mock_open()) as patched_open:
        test_settings.save_settings()
    patched_open.assert_called_with(file=fake_files[0], mode='w')


def test_09_save_file_failed(monkeypatch):
    """
    Test the save_settings function is working as expected

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

    def mock_failed(file, mode):
        """
        Fake a failure

        Args:
            file (_type_): _description_
            mode (_type_): _description_
        """
        raise Exception("Well this was totally expected")

    # Patch in the does_exist
    monkeypatch.setattr(file_man, "does_exist", mock_exists)
    test_settings = MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    # Patch again,this time for the save operation
    with patch("builtins.open", mock_failed):
        with pytest.raises(Exception):
            assert test_settings.save_settings()


def test_10_set_item(monkeypatch):
    """
    Test the __setitem__ function is working as expected

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

    # Patch in the does_exist
    monkeypatch.setattr(file_man, "does_exist", mock_exists)
    test_settings = MacSettings(
        settings_file_path=fake_files[0],
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    # The asserts will test the __getitem__ function
    assert test_settings['fake_load'] == settings_dict['fake_load']
    assert test_settings['something', 'else'] == settings_dict[
        'something']['else']

    # Now change the settings and start again
    with patch("builtins.open", mock_open()):
        test_settings['fake_load'] = 'fake changed'
        test_settings['something', 'else'] = 'something changed'
    assert test_settings['fake_load'] == 'fake changed'
    assert test_settings['something', 'else'] == 'something changed'


def test_11_contains_success(monkeypatch):
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

    assert "fake_load" in test_settings
    assert ("something", "else") in test_settings
    assert "made-up" not in test_settings
    assert ("made-up", "deeper") not in test_settings
    assert ("something", "unknown") not in test_settings
    assert ("something", "else", "unknown") not in test_settings


def test_12_contains_failed(monkeypatch):
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
    with pytest.raises(MacSettingsException):
        assert ['str1', 'str2'] in test_settings

# def test_12_contains_failed(monkeypatch):
#     """
#     Test the load settings function works

#     Args:
#         monkeypatch (_type_): _description_
#     """
#     global fake_files
#     global settings_dict

#     def mock_exists(os_path):
#         """
#         Make sure the file name passed is known about  and
#         return true.

#         Args:
#             faked_name (str): File Name to check
#         """
#         assert os_path in fake_files
#         return True


#     monkeypatch.setattr(file_man, "does_exist", mock_exists)


if __name__ == "__main__":  # pragma: no cover
    pass
