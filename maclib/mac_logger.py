#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_logger.py
    Desscription:
        Setup logging to include:
         - ISO8601 date formatting.
         - Optional use UTC.
         - Render as SYSLOG or JSON.
         - Rotate log files at 1MB, keeps the last 5.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import os
import sys
import logging
import logging.handlers
import time
import inspect
from pathlib import Path

FORMAT_SYSLOG = 1
FORMAT_JSON = 2

LOGGER_NAME = Path(inspect.stack()[-1][1]).stem


def configure_logger(log_file_uri: str = None,
                     logging_level: int = logging.INFO,
                     logger_name: str = LOGGER_NAME,
                     use_stdout: bool = True,
                     use_utc: bool = True,
                     use_format: int = FORMAT_SYSLOG) -> logging.Logger:
    """
    Setup the built in logger to work as we want it.

    :arg log_file_uri: Where we want to make our log file
    :arg logging_level: What level do we want to start logging at?
                        Default is set to INFO
    :arg logger_name: Set the logger name. The default will be the name of the
                      process. It can overridden here, but wn't be persistent.
    :arg use_stdout: Flag to show whether to output to stdout or not.
    :arg use_utc: Log timestamp will use UTC. False by default
    :arg use_format: Format the output as SYSLOG or JSON. Default is SYSLOG.
    """
    # We may not need a file, so only configure it if it's been set.
    # Otherwise just dump to the console.
    log_formatter: logging.Formatter
    mac_logger: logging.Logger
    log_file_handler: logging.Handler
    format_config: str
    date_config: str

    if use_format is FORMAT_JSON:
        if use_utc:
            format_config = "{ event_time : \"%(asctime)s.%(msecs)03dZ\"" \
                            ",level : \"%(levelname)s\", function_name: \"" \
                            "%(module)s.%(funcName)s\", message: \"" \
                            "%(message)s\" }"
        else:
            format_config = "{ event_time : \"%(asctime)s.%(msecs)03d\", " \
                            "level : \"%(levelname)s\", function_name: \"" \
                            " %(module)s.%(funcName)s\", message: \"" \
                            "%(message)s\" }"
    else:
        if use_utc:
            format_config = "%(asctime)s.%(msecs)03dZ %(levelname)s " \
                            "%(module)s.%(funcName)s %(message)s"
        else:
            format_config = "%(asctime)s.%(msecs)03d %(levelname)s " \
                            "%(module)s.%(funcName)s %(message)s"

    date_config = "%Y-%m-%dT%H:%M:%S"

    log_formatter = logging.Formatter(
            fmt=format_config,
            datefmt=date_config
        )
    if use_utc:
        log_formatter.converter = time.gmtime
    mac_logger = logging.getLogger(name=logger_name)

    if log_file_uri:
        # Check the logging directory is available.
        # If not create it.
        if not os.path.isdir(os.path.dirname(log_file_uri)):
            try:
                os.makedirs(os.path.dirname(log_file_uri))
            except OSError as o_error:
                print("Unable to create the logging directory "
                      "{0}.\n{1}".format(os.path.dirname(log_file_uri),
                                         o_error.strerror))
                sys.exit(1)
        log_file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file_uri,
            maxBytes=1240000,
            backupCount=5)
    else:
        log_file_handler = logging.StreamHandler()
    log_file_handler.setFormatter(fmt=log_formatter)
    mac_logger.addHandler(hdlr=log_file_handler)
    # User can supress console spam, but the log file will still be
    # written to.
    if use_stdout:
        log_std_out = logging.StreamHandler(stream=sys.stdout)
        log_std_out.setFormatter(fmt=log_formatter)
        mac_logger.addHandler(hdlr=log_std_out)
    mac_logger.setLevel(level=logging_level)
    return mac_logger


if __name__ == "__main__":
    pass
