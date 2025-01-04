#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_logger.py
    Description:
        Setup logging to include:
         - ISO8601 date formatting.
         - Render as SYSLOG or JSON.
         - Rotate log files at 1MB, keeps the last 5.
         - Automatic Windows Event Log support
    Version:
        2 - The time stamp is now fully ISO 8601 compliant, removing the
            use_utc flag as it's no longer needed. All times are UTC with
            the offset shown for local time.
          - Added Windows Event Log support instead of writing to a file.
          - Added support for macOS X
          - Automatically places the log file in the correct folder for the
            platform.
        1 - Initial release
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


def configure_logger(
    app_name: str = None,
    logging_level: int = logging.INFO,
    logger_name: str = LOGGER_NAME,
    console_only: bool = False,
    suppress_console: bool = False,
    use_format: int = FORMAT_SYSLOG,
) -> logging.Logger:
    """
    Setup the built in logger to work as we want it.

    Args:
        app_name (str): The name given to the application.
        logging_level (int): The logging level. Default is INFO.
        logger_name (str): The logger name. Default is the name of the process.
        console_only (bool): If True, log only to the console.
        suppress_console (bool): If True, suppress console logging.
        use_format (int): Format the output as SYSLOG or JSON. Default is SYSLOG.

    Returns:
        logging.Logger: A fully configured persistent logger.
    """
    # We may not need a file, so only configure it if it's been set.
    # Otherwise just dump to the console.
    log_formatter: logging.Formatter
    mac_logger: logging.Logger
    log_file_handler: logging.Handler
    log_file_uri: str
    format_config: str
    date_config: str
    tz: str = time.strftime("%z")

    if use_format == FORMAT_JSON:
        format_config = (
            '{ event_time : "%(asctime)s.%(msecs)03dZ'
            + tz
            + '", level: "%(levelname)s", function_name: "'
            '%(module)s.%(funcName)s", message: "'
            '%(message)s" }'
        )
    else:
        format_config = (
            "%(asctime)s.%(msecs)03dZ" + tz + " %(levelname)s "
            "%(module)s.%(funcName)s %(message)s"
        )

    # ISO8601 Time format
    date_config = "%Y-%m-%dT%H:%M:%S"

    # Create the log formatter. use the same format across all platforms.
    # I know Windows does it's own thing, but this way the log event
    # will look the same regardless of environment.
    log_formatter = logging.Formatter(fmt=format_config, datefmt=date_config)
    log_formatter.converter = time.gmtime
    mac_logger = logging.getLogger(name=logger_name)

    # Added support for macOS X as well as Linux/BSD
    if "darwin" == sys.platform:  # pragma: no cover
        log_file_uri = os.path.expanduser("~/Library/Logs")
        log_file_uri = f"{log_file_uri}/{app_name}/{app_name}.log"
    else:
        log_file_uri = os.path.expanduser("~/.local/state")
        log_file_uri = f"{log_file_uri}/{app_name}/{app_name}.log"

    if console_only:
        log_file_handler = logging.StreamHandler()
    elif "win32" == sys.platform:  # pragma: no cover
        # On Windows log records go to the Windows Event Log.
        # Worth noting that debug messages will appear as
        # Information messages in the application Event Log.
        log_file_handler = logging.handlers.NTEventLogHandler(
            appname=app_name, logtype="Application"
        )
    else:
        # Check the logging directory is available.
        # If not create it.
        if not os.path.isdir(os.path.dirname(log_file_uri)):
            try:
                os.makedirs(os.path.dirname(log_file_uri))
            except OSError as o_error:
                print(
                    "Unable to create the logging directory "
                    f"{os.path.dirname(log_file_uri)}.\n{o_error.strerror}"
                )
                sys.exit(1)
        log_file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file_uri, maxBytes=1048576, backupCount=5
        )
    log_file_handler.setFormatter(fmt=log_formatter)

    mac_logger.addHandler(hdlr=log_file_handler)
    # User can supress console spam, but the log file will still be
    # written to.
    if not suppress_console:
        log_std_out = logging.StreamHandler(stream=sys.stdout)
        log_std_out.setFormatter(fmt=log_formatter)
        mac_logger.addHandler(hdlr=log_std_out)

    mac_logger.setLevel(level=logging_level)
    return mac_logger


if __name__ == "__main__":  # pragma: no cover
    pass
