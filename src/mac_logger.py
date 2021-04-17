#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_logger.py
    Desscription:
        Setup logging.
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


def configure_logger(log_file_uri: str = None,
                     logging_level: int = logging.INFO,
                     use_stdout: bool = True) -> logging.Logger:
    """
    Setup the built in logger to work as we want it.

    :arg log_file_uri: Where we want to make our log file
    :arg logging_level: What level do we want to start logging at?
                        Default is set to INFO
    :arg use_stdout: Flag to show whether to output to stdout or not.
    """
    # We may not need a file, so only configure it if it's been set.
    # Otherwise just dump to the console.
    log_formatter: logging.Formatter
    mac_logger: logging.Logger
    log_file_handler: logging.Handler

    log_formatter = logging.Formatter(
            fmt="{ event_time : \"%(asctime)s.%(msecs)03d\", level : \"%("
                "levelname)s\", function_name: \"%(module)s.%(funcName)s\","
                " message: \"%(message)s\" }",
            datefmt="%Y-%m-%dT%H:%M:%S"
        )
    mac_logger = logging.getLogger(name='mac_logger')

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
