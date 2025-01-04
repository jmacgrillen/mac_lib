#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_exception.py
    Description:
        Base exception class that includes capturing the exception in the log.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import logging
import maclib.mac_logger as mac_logger


class MacException(Exception):
    """
    Base exception class for mac_lib. Pushes out
    exceptions to the log file.
    """
    def __init__(self, str_message: str):
        """
        Raise the exception just like normal.

        Args:
            str_message (str):
                The message to log and display back to the user.
        """
        m_logger = logging.getLogger(mac_logger.LOGGER_NAME)
        str_message = f"Exception - {str_message}"
        m_logger.error(str_message)
        super(MacException, self).__init__(str_message)


if __name__ == "__main__":  # pragma: no cover
    pass
