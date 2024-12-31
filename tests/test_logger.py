#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        test_logger.py
    Desscription:
        Test the custom logger configuration.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import pytest
import os
import time
import logging
import maclib.mac_logger as mlogger


def test_logger_01_json_utc():
    """
    Test the JSON format is correct.
    """
    tz: str = time.strftime('%z')
    format_config = "{ event_time : \"%(asctime)s.%(msecs)03dZ" + tz + \
                    "\", level: \"%(levelname)s\", function_name: \"" \
                    "%(module)s.%(funcName)s\", message: \"" \
                    "%(message)s\" }"

    logger_name = "test_logger_json_utc"

    test_logger = mlogger.configure_logger(
        logger_name=logger_name,
        use_format=mlogger.FORMAT_JSON
    )

    assert test_logger.handlers[0].formatter._fmt == format_config


def test_logger_02_syslog_utc():
    """
    Test the SYSLOG format is correct.
    """
    tz: str = time.strftime('%z')
    format_config = "%(asctime)s.%(msecs)03dZ" + tz + " %(levelname)s " \
                    "%(module)s.%(funcName)s %(message)s"
    logger_name = "test_logger_syslog_utc"

    test_logger = mlogger.configure_logger(
        logger_name=logger_name,
        use_format=mlogger.FORMAT_SYSLOG
    )

    assert test_logger.handlers[0].formatter._fmt == format_config


def test_logger_03_to_file(monkeypatch, tmp_path):
    """
    Test the stdout config is missing.
    """
    app_name: str = "LoggerTest"
    logger_name: str = "test_logger_syslog_to_file"
    logger_file_name: str = f"{tmp_path}/.local/state/" \
                            f"{app_name}/{app_name}.log"
    monkeypatch.setenv('HOME', str(tmp_path))

    test_logger = mlogger.configure_logger(
        app_name=app_name,
        logger_name=logger_name,
        use_format=mlogger.FORMAT_SYSLOG
    )

    assert test_logger.handlers[0].baseFilename == str(logger_file_name)


def test_logger_04_syslog_no_file_exist(monkeypatch, tmp_path):
    """
    Test the stdout config is missing.
    """
    app_name: str = "LoggerTest"
    logger_name: str = "test_logger_syslog_no_exist"
    logger_directory: str = f"{tmp_path}/.local/state/{app_name}"

    def isdir_output(os_path: str):
        """
        Make sure this comes back as false
        """
        print
        assert os_path == logger_directory
        return False

    def makedirs_output(os_path: str):
        """
        Make sure there's no OSError from makedirs
        """
        assert os_path == logger_directory
        return None

    monkeypatch.setattr(os, "makedirs", makedirs_output)
    monkeypatch.setattr(os.path, 'isdir', isdir_output)
    monkeypatch.setenv('HOME', str(tmp_path))

    with pytest.raises(OSError):
        assert mlogger.configure_logger(
            app_name=app_name,
            logger_name=logger_name,
            use_format=mlogger.FORMAT_SYSLOG)


def test_logger_05_syslog_file_create_error(monkeypatch, tmp_path):
    """
    Test the stdout config is missing.
    """
    app_name: str = "LoggerTest"
    logger_name: str = "test_logger_syslog_no_exist"
    logger_directory: str = f"{tmp_path}/.local/state/{app_name}"

    def isdir_output(os_path: str):
        """
        Make sure this comes back as false
        """
        print
        assert os_path == logger_directory
        return False

    def makedirs_output(os_path: str):
        """
        Make sure there's no OSError from makedirs
        """
        assert os_path == logger_directory
        raise OSError('Not doing it')

    monkeypatch.setattr(os, "makedirs", makedirs_output)
    monkeypatch.setattr(os.path, 'isdir', isdir_output)
    monkeypatch.setenv('HOME', str(tmp_path))

    with pytest.raises(SystemExit):
        assert mlogger.configure_logger(
            app_name=app_name,
            logger_name=logger_name,
            use_format=mlogger.FORMAT_SYSLOG) == 1


def test_logger_06_console_only(monkeypatch, tmp_path):
    """
    Test the stdout config is missing.
    """
    app_name: str = "LoggerTest"
    logger_name: str = "test_logger_syslog_no_exist"

    monkeypatch.setenv('HOME', str(tmp_path))

    test_logger = mlogger.configure_logger(
                    app_name=app_name,
                    logger_name=logger_name,
                    console_only=True,
                    use_format=mlogger.FORMAT_SYSLOG)
    assert type(test_logger.handlers[0]) == logging.StreamHandler


if __name__ == "__main__":  # pragma: no cover
    pass
