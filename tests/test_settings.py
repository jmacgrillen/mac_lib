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
import maclib.mac_settings as settings
import maclib.mac_file_management as file_man


def test_01_settings_default_exist(monkeypatch):
    """
    Test the logic works when the settings files exist

    Args:
        monkeypatch (_type_): _description_
    """
    fake_files = ["mysettings.yaml", "defaults.yaml"]

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
    test_settings = settings.MacSettings(
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
    fake_files = ["mysettings.yaml", "defaults.yaml"]

    with pytest.raises(settings.MacSettingsException):
        assert settings.MacSettings(
           settings_file_path=fake_files[0],
           default_settings_path=fake_files[1])


if __name__ == "__main__":  # pragma: no cover
    pass
