#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
import shutil
import os
import watchdog.observers
from unittest.mock import mock_open, patch
from maclib.mac_settings import (MacSettings,
                                 MacSettingsException,
                                 MacSettingsWatchdogHandler)
import maclib.mac_file_management as file_m


app_name = 'test_app'
fake_files = [os.path.expanduser(f"~/.config/{app_name}/{app_name}.yaml"),
              "defaults.yaml", "meh.yaml"]
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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])
    assert test_settings.settings_file_path == fake_files[0]
    assert test_settings.default_settings_path == fake_files[1]
    MacSettings.clear()


def test_02_defaults_not_exist():
    """
    Test the logic works when the default settings file
    does not exist

    Args:
        monkeypatch (_type_): _description_
    """
    global fake_files

    with pytest.raises(MacSettingsException):
        MacSettings(
            app_name=app_name,
            default_settings_path="mouse")
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    monkeypatch.setattr(MacSettings,
                        "_copy_default_settings",
                        copy_file)
    MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)

    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    assert test_settings.settings_file_path == fake_files[0]
    assert test_settings.default_settings_path == fake_files[1]
    assert test_settings.get_all_settings() == settings_dict
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)

    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    with patch("builtins.open", mock_open(read_data=str_yaml)):
        with pytest.raises(MacSettingsException):
            assert test_settings.load_settings()
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    # The asserts will test the __getitem__ function
    assert test_settings['fake_load'] == settings_dict['fake_load']
    assert test_settings['something', 'else'] == settings_dict[
        'something']['else']
    MacSettings.clear()


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

    def copy_file(self):
        """
        Fake the file copy
        """
        pass

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    with pytest.raises(MacSettingsException):
        assert test_settings['not-there']
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    # Patch again,this time for the save operation
    with patch("builtins.open", mock_open()) as patched_open:
        test_settings.save_settings()
    patched_open.assert_called_with(file=fake_files[0], mode='w')
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    # Now make it look like the open command is returning a YAML string
    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    # Patch again,this time for the save operation
    with patch("builtins.open", mock_failed):
        with pytest.raises(Exception):
            assert test_settings.save_settings()
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    test_settings = MacSettings(
        app_name=app_name,
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
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)

    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()

    assert "fake_load" in test_settings
    assert ("something", "else") in test_settings
    assert "made-up" not in test_settings
    assert ("made-up", "deeper") not in test_settings
    assert ("something", "unknown") not in test_settings
    assert ("something", "else", "unknown") not in test_settings
    MacSettings.clear()


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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)

    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    with patch("builtins.open", mock_open(read_data=str(settings_dict))):
        test_settings.load_settings()
    with pytest.raises(MacSettingsException):
        assert ['str1', 'str2'] in test_settings
    MacSettings.clear()


def test_13_copy_defaults(monkeypatch):
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

    def mock_dir_exist(os_path):
        """
        Make sure the file name passed is known about  and
        return true.

        Args:
            faked_name (str): File Name to check
        """
        return True

    def mock_copy(src, dst):
        """
        shutils file copy mock

        Args:
            src (_type_): _description_
            dst (_type_): _description_

        Returns:
            _type_: _description_
        """
        assert src == fake_files[1]
        assert dst == fake_files[0]
        return True

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)

    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    monkeypatch.setattr(shutil, "copyfile", mock_copy)
    monkeypatch.setattr(file_m, "does_exist", mock_dir_exist)
    test_settings._copy_default_settings()
    MacSettings.clear()


def test_14_copy_create_directory(monkeypatch):
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

    def mock_dir_exist(os_path):
        """
        Make sure the file name passed is known about  and
        return true.

        Args:
            faked_name (str): File Name to check
        """
        return False

    def mock_copy(src, dst):
        """
        shutils file copy mock

        Args:
            src (_type_): _description_
            dst (_type_): _description_

        Returns:
            _type_: _description_
        """
        assert src == fake_files[1]
        assert dst == fake_files[0]
        return True

    def mock_create(dir):
        """
        shutils file copy mock

        Args:
            src (_type_): _description_
            dst (_type_): _description_

        Returns:
            _type_: _description_
        """
        return True

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])

    monkeypatch.setattr(shutil, "copyfile", mock_copy)
    monkeypatch.setattr(file_m, "does_exist", mock_dir_exist)
    monkeypatch.setattr(file_m, "create_dir", mock_create)
    test_settings._copy_default_settings()
    MacSettings.clear()


def test_15_test_callback_registered(monkeypatch):
    """
    Test whether the register callback feature works

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

    def mock_observer(arg):
        """
        Create a mock observer object

        Args:
            os_path (_type_): _description_
        """
        assert type(arg) is watchdog.observers.inotify.InotifyObserver

    def my_call_back():
        """
        Simple callback
        """
        pass

    # Patch in the does_exist
    monkeypatch.setattr(watchdog.observers.Observer, "start", mock_observer)
    monkeypatch.setattr(file_m, "does_exist", mock_exists)
    test_settings = MacSettings(
        app_name=app_name,
        default_settings_path=fake_files[1])
    test_settings.register_for_events("settings_change", my_call_back)
    assert my_call_back in test_settings.events_publisher.subscribers[
        "settings_change"]
    MacSettings.clear()


def test_18_test_watchdog_handler_no_pause(monkeypatch):
    """
    Test whether the register callback feature works

    Args:
        monkeypatch (_type_): _description_
    """
    class MockedMacSettings():
        _load_called = False
        _execute_called = False

        def __init__(self) -> None:
            pass

        def load_settings(self):
            self._load_called = True

        def _execute_callbacks(self):
            self._execute_called = True

    mocked_event = 'Mocked'

    mock_settings = MockedMacSettings()
    test_handler = MacSettingsWatchdogHandler()
    test_handler._pause_observer = False
    test_handler.on_modified(mocked_event)
    assert mock_settings._load_called is True
    assert mock_settings._execute_called is True


def test_19_test_watchdog_handler_paused(monkeypatch):
    """
    Test whether the register callback feature works

    Args:
        monkeypatch (_type_): _description_
    """
    class MockedMacSettings():
        _load_called = False
        _execute_called = False

        def __init__(self) -> None:
            pass

        def load_settings(self):
            self._load_called = True

        def _execute_callbacks(self):
            self._execute_called = True

    mocked_event = 'Mocked'

    mock_settings = MockedMacSettings()
    test_handler = MacSettingsWatchdogHandler(mock_settings)
    test_handler._pause_observer = True
    test_handler.on_modified(mocked_event)
    assert mock_settings._load_called is False
    assert mock_settings._execute_called is False


if __name__ == "__main__":  # pragma: no cover
    pass
