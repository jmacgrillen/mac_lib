#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_file_management.py
    Description:
        The Mac Library settinsg file manager.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import os
from pathlib import Path
import logging
import maclib.mac_logger as mac_logger
from maclib.mac_exception import MacException


file_logging: logging.Logger = logging.getLogger(mac_logger.LOGGER_NAME)


class FileDoesNotExistException(MacException):
    """
    As file does not exist is a useful exception lets create
    a resusable one here.
    """

    pass


def does_exist(os_path: str) -> bool:
    """
    Check whether the file exists.

    Args:
        os_path (str):
            The full os path to the directory/file.

    Return:
        bool:
            True if the os_path exists, otherwise False.
    """
    return Path(os_path).exists()


def can_read(os_path: str) -> bool:
    """
    Check whether the file can be read from.

    Args:
        os_path (str):
            The full path to the directory/file

    Return:
        bool:
            True if we have read access to os_path, otherwise false.
    """
    return os.access(path=os_path, mode=os.R_OK)


def can_write_to(os_path: str) -> bool:
    """
    Check whether the file object can be written to.

    Args:
        os_path (str):
            The full path to the directiry/file.

    Return:
        bool:
            True if we have write access to os_path, otherwise false.
    """
    return os.access(path=os_path, mode=os.W_OK)


def get_parent_dir(os_path: str) -> str:
    """
    Get the parent directory.

    Args:
        os_path (str):
            The full path to the directoy/path.

    Return:
        str:
            The full path of the parent directory.
    """
    return str(Path(os_path).parents[1])


def delete_file(os_path: str) -> bool:
    """
    Delete the selected file.

    Args:
        os_path (str):
            The full path to the directory/path.

    Return:
        bool:
            True if the file was deleted, false otherwise.
    """
    if does_exist(os_path):
        file_logging.info(f"Deleting file {os_path}")
        try:
            os.remove(os_path)
            return True
        except OSError as e:
            file_logging.error(f"Could not delete file {os_path}. {e}")
    else:
        file_logging.info(f"Unable to delete {os_path} as it does not exist.")
    return False


def create_dir(dir_path: str) -> bool:
    """
    Create a new directory.

    Args:
        dir_path (str):
            The name of the directory we want to create.

    Return:
        bool:
            True if the directory was successfully created, otherwise false.
    """
    if not does_exist(dir_path):
        if can_write_to(get_parent_dir(dir_path)):
            try:
                os.makedirs(name=dir_path)
                return True
            except OSError:
                file_logging.error("Unable to create the directory")
                return False
        else:
            err_msg = (
                "Do not have permssions to create directory "
                f"under {get_parent_dir(dir_path)}"
            )
            file_logging.error(err_msg)
            return False
    else:
        file_logging.info(f"Directory {dir_path} already exists.")
    return False


if __name__ == "__main__":  # pragma: no cover
    pass
