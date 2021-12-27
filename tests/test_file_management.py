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
    fake_path = "test"

    def mock_exists(faked_exist):
        """
        Check the path is being passed correctly and
        return true.
        """
        assert f"{faked_exist.name}" == fake_path
        return True

    monkeypatch.setattr(Path, "exists", mock_exists)
    assert fm.does_exist(fake_path) is True


def test_fm_02_exists_false(monkeypatch):
    """
    Test the does_exist function returns false
    """
    fake_path = "test"

    def mock_exists(faked_exist):
        """
        Check the path is being passed correctly and
        return false.
        """
        assert f"{faked_exist.name}" == fake_path
        return False

    monkeypatch.setattr(Path, "exists", mock_exists)
    assert fm.does_exist(fake_path) is False


def test_fm_03_can_read_true(monkeypatch):
    """
    Test the can read function returns true
    """
    fake_path = "test"

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
    fake_path = "test"

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
    fake_path = "test"

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
    fake_path = "test"

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


def test_fm_09_delete_file_true(tmp_path):
    """
    Test the delete function
    """
    temp_path = tmp_path / "test.txt"
    with open(temp_path, 'w') as file_p:
        file_p.write('Test\n')
    assert fm.delete_file(temp_path) is True


def test_fm_10_delete_file_no_file():
    """
    Test what happens when delete fails
    """
    assert fm.delete_file("nofile.txt") is False


def test_fm_11_delete_file_failed(monkeypatch):
    """
    Test that OSError is handled
    """
    test_file_name = "nofile.txt"

    def does_exist_true(os_path: str):
        """
        Make sure we get a True returned.
        """
        assert os_path == test_file_name
        return True

    def remove_response(os_path: str):
        """
        Make sure that OSError is raised
        """
        assert os_path == test_file_name
        raise OSError("This is a test.")

    monkeypatch.setattr(fm, 'does_exist', does_exist_true)
    monkeypatch.setattr(os, 'remove', remove_response)
    assert fm.delete_file(test_file_name) is False


def test_fm_12_create_dir(tmp_path):
    """
    Test that does_exist is being properly invoked.
    """
    test_dir_name = tmp_path / "mytest"
    assert fm.create_dir(test_dir_name) is True


def test_fm_12_create_dir_already_exists(monkeypatch):
    """
    Test that does_exist is being properly invoked.
    """
    test_dir_name = "test_dir/mytest"

    def does_exist_true(dir_name: str):
        """
        Return True to test the creation fails.
        """
        assert dir_name == test_dir_name
        return True

    monkeypatch.setattr(fm, 'does_exist', does_exist_true)
    assert fm.create_dir(test_dir_name) is False


def test_fm_12_create_dir_cant_write(monkeypatch):
    """
    Test that does_exist is being properly invoked.
    """
    test_dir_name = "/home/test_dir/test_dir_name"

    def does_exist_false(dir_name: str):
        """
        Return True to test the creation fails.
        """
        assert dir_name == test_dir_name
        return False

    def can_write_false(dir_name: str):
        """
        Return True to test the creation fails.
        """
        assert Path(dir_name) == Path('/home')
        return False

    monkeypatch.setattr(fm, 'does_exist', does_exist_false)
    monkeypatch.setattr(fm, 'can_write_to', can_write_false)
    assert fm.create_dir(test_dir_name) is False


def test_fm_12_create_dir_exception(monkeypatch):
    """
    Test that does_exist is being properly invoked.
    """
    test_dir_name = "/home/test_dir/mytest"

    def does_exist_false(dir_name: str):
        """
        Return True to test the creation fails.
        """
        assert dir_name == test_dir_name
        return False

    def can_write_true(dir_name: str):
        """
        Return True to test the creation fails.
        """
        assert dir_name == "\\home"
        return True

    def makedirs_exception(name: str):
        """
        Raise an OSError to make sure it's handled
        """
        assert name == test_dir_name
        raise OSError("Test Exception")

    monkeypatch.setattr(fm, 'does_exist', does_exist_false)
    monkeypatch.setattr(fm, 'can_write_to', can_write_true)
    monkeypatch.setattr(os, 'makedirs', makedirs_exception)
    assert fm.create_dir(test_dir_name) is False


if __name__ == "__main__":
    pass
