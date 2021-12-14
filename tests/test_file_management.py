#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        test_file_management.py
    Desscription:
        Test the functions in the file management library.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import pytest
from pathlib import Path
import os
import maclib.mac_file_management as fm


def test_fm_01_exists_true(monkeypatch):
    """
    Test the does_exist function returns true
    """
    fake_path = "\\test"

    def mock_exists(faked_exist):
        """
        Check the path is being passed correctly and
        return true.
        """
        assert f"\\{faked_exist.name}" == fake_path
        return True

    monkeypatch.setattr(Path, "exists", mock_exists)
    assert fm.does_exist(fake_path) is True


def test_fm_02_exists_false(monkeypatch):
    """
    Test the does_exist function returns false
    """
    fake_path = "\\test"

    def mock_exists(faked_exist):
        """
        Check the path is being passed correctly and
        return false.
        """
        assert f"\\{faked_exist.name}" == fake_path
        return False

    monkeypatch.setattr(Path, "exists", mock_exists)
    assert fm.does_exist(fake_path) is False


def test_fm_03_can_read_true(monkeypatch):
    """
    Test the can read function returns true
    """
    fake_path = "\\test"

    def mock_access(path, mode):
        """
        Check the path and mode are being passed correctly
        and return true.
        """
        assert path == fake_path
        assert mode == os.R_OK
        return True

    monkeypatch.setattr(os, 'access', mock_access)
    assert fm.can_read(fake_path) is True


def test_fm_04_can_read_false(monkeypatch):
    """
    Test the can read function returns false
    """
    fake_path = "\\test"

    def mock_access(path, mode):
        """
        Check the path and mode are being passed correctly
        and return false.
        """
        assert path == fake_path
        assert mode == os.R_OK
        return False

    monkeypatch.setattr(os, 'access', mock_access)
    assert fm.can_read(fake_path) is False


def test_fm_05_can_write_true(monkeypatch):
    """
    Test the can write function returns true
    """
    fake_path = "\\test"

    def mock_access(path, mode):
        """
        Check the path and mode are being passed correctly
        and return true.
        """
        assert path == fake_path
        assert mode == os.W_OK
        return True

    monkeypatch.setattr(os, 'access', mock_access)
    assert fm.can_write_to(fake_path) is True


def test_fm_06_can_write_false(monkeypatch):
    """
    Test the can write function returns false
    """
    fake_path = "\\test"

    def mock_access(path, mode):
        """
        Check the path and mode are being passed correctly
        and return false.
        """
        assert path == fake_path
        assert mode == os.W_OK
        return False

    monkeypatch.setattr(os, 'access', mock_access)
    assert fm.can_write_to(fake_path) is False


def test_fm_07_parent_dir_correct_path():
    """
    Test the parent directory is being returned
    """
    test_path = 'PYTEST_TMPDIR/test_directory/testfile.txt'
    assert fm.get_parent_dir(test_path) == 'PYTEST_TMPDIR'


def test_fm_08_parent_dir_file_name_only():
    """
    When being fed a file name this should raise an exception
    """
    test_path = 'testfile.txt'
    with pytest.raises(IndexError):
        assert fm.get_parent_dir(test_path)


def test_fm_09_delete_file_true():
    """
    Test the delete function
    """
    test_path = 'PYTEST_TMPDIR/testfile.txt'
    assert fm.delete_file(test_path) is True
