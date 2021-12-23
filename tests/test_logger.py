#! /usr/bin/env python -*- coding: utf-8 -*-
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
import maclib.mac_logger as mlogger


def test_logger_01_json_utc():
    """
    Test the JSON format is correct.
    """
    format_config = "{ event_time : \"%(asctime)s.%(msecs)03dZ\"" \
                    ",level : \"%(levelname)s\", function_name: \"" \
                    "%(module)s.%(funcName)s\", message: \"" \
                    "%(message)s\" }"
    logger_name = "test_logger_json_utc"

    test_logger = mlogger.configure_logger(
        logger_name=logger_name,
        use_format=mlogger.FORMAT_JSON
    )

    assert test_logger.handlers[0].formatter._fmt == format_config


def test_logger_02_json_bst():
    """
    Test the JSON format is correct.
    """
    format_config = "{ event_time : \"%(asctime)s.%(msecs)03d\", " \
                    "level : \"%(levelname)s\", function_name: \"" \
                    " %(module)s.%(funcName)s\", message: \"" \
                    "%(message)s\" }"
    logger_name = "test_logger_json_bst"

    test_logger = mlogger.configure_logger(
        logger_name=logger_name,
        use_format=mlogger.FORMAT_JSON,
        use_utc=False
    )

    assert test_logger.handlers[0].formatter._fmt == format_config


def test_logger_03_syslog_utc():
    """
    Test the SYSLOG format is correct.
    """
    format_config = "%(asctime)s.%(msecs)03dZ %(levelname)s " \
                    "%(module)s.%(funcName)s %(message)s"
    logger_name = "test_logger_syslog_utc"

    test_logger = mlogger.configure_logger(
        logger_name=logger_name,
        use_format=mlogger.FORMAT_SYSLOG
    )

    assert test_logger.handlers[0].formatter._fmt == format_config


def test_logger_04_syslog_bst():
    """
    Test the SYSLOG format is correct.
    """
    format_config = "%(asctime)s.%(msecs)03d %(levelname)s " \
                    "%(module)s.%(funcName)s %(message)s"
    logger_name = "test_logger_syslog_bst"

    test_logger = mlogger.configure_logger(
        logger_name=logger_name,
        use_format=mlogger.FORMAT_SYSLOG,
        use_utc=False
    )
    assert test_logger.handlers[0].formatter._fmt == format_config


def test_logger_05_to_file(tmp_path):
    """
    Test the stdout config is missing.
    """
    logger_name = "test_logger_syslog_to_file"
    logger_file_name = tmp_path / "test.txt"

    test_logger = mlogger.configure_logger(
        logger_name=logger_name,
        use_format=mlogger.FORMAT_SYSLOG,
        log_file_uri=logger_file_name
    )

    assert test_logger.handlers[0].baseFilename == str(logger_file_name)


def test_logger_06_to_file_not_exists(monkeypatch, tmp_path):
    """
    Test the stdout config is missing.
    """
    logger_name = "test_logger_syslog_no_exist"
    logger_file_name = tmp_path / "test.txt"

    def isdir_output(os_path: str):
        """
        Make sure this comes back as false
        """
        assert os_path == str(tmp_path)
        return False

    def makedirs_output(os_path: str):
        """
        Make sure there's no OSError from makedirs
        """
        assert os_path == str(tmp_path)
        return None

    monkeypatch.setattr(os, "makedirs", makedirs_output)
    monkeypatch.setattr(os.path, 'isdir', isdir_output)
    test_logger = mlogger.configure_logger(
        logger_name=logger_name,
        use_format=mlogger.FORMAT_SYSLOG,
        log_file_uri=logger_file_name
    )

    assert test_logger.handlers[0].baseFilename == str(logger_file_name)


def test_logger_07_exception(monkeypatch, tmp_path):
    """
    Test the stdout config is missing.
    """
    logger_name = "test_logger_syslog_no_exist"
    logger_file_name = tmp_path / "test.txt"

    def isdir_output(os_path: str):
        """
        Make sure this comes back as false
        """
        assert os_path == str(tmp_path)
        return False

    monkeypatch.setattr(os.path, 'isdir', isdir_output)
    with pytest.raises(SystemExit) as expected_exit:
        mlogger.configure_logger(
            logger_name=logger_name,
            use_format=mlogger.FORMAT_SYSLOG,
            log_file_uri=logger_file_name
        )

    assert expected_exit.type == SystemExit
    assert expected_exit.value.code == 1
