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
        3 - Changed the way the logger is configured to use a
            StreamHandler for console output, which allows for better
            control over console logging.
          - Added a check to avoid adding multiple StreamHandlers to the logger.
          - Updated the log format to include milliseconds in the timestamp.
          - Changed the default logging level to INFO.
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
from enum import IntEnum

class FormatType(IntEnum):
    """
    Enum for the different logging formats available.
    """
    SYSLOG = 1
    JSON = 2

LOGGER_NAME = Path(inspect.stack()[-1][1]).stem


def configure_logger(
    app_name: str,
    logging_level: int = logging.INFO,
    logger_name: str = LOGGER_NAME,
    console_only: bool = False,
    suppress_console: bool = False,
    use_format: FormatType = FormatType.SYSLOG,
) -> logging.Logger:
    """
    Setup the built in logger to work as we want it.

    Args:
        app_name (str): The name given to the application.
        logging_level (int): The logging level. Default is INFO.
        logger_name (str): The logger name. Default is the name of the process.
        console_only (bool): If True, log only to the console.
        suppress_console (bool): If True, suppress console logging.
        use_format (FormatType): The format for log output (SYSLOG or JSON).
                                 Default is SYSLOG.

    Returns:
        logging.Logger: A fully configured persistent logger.
    """
    # We may not need a file, so only configure it if it's been set.
    # Otherwise just dump to the console.
    log_formatter: logging.Formatter
    mac_logger: logging.Logger
    log_file_dir: Path
    log_file_uri: Path
    format_config: str
    date_config: str
    tz: str = time.strftime("%z")

    if use_format == FormatType.JSON:
        format_config = (
            '{ "event_time": "%(asctime)s.%(msecs)03dZ", "level": '
            '"%(levelname)s", "function_name": "%(module)s.%(funcName)s", '
            '"message": "%(message)s" }')
    else: # Default to SYSLOG format
        format_config = (
            "%(asctime)s.%(msecs)03dZ %(levelname)s "
            "%(module)s.%(funcName)s %(message)s")

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
        log_file_dir = Path(os.path.expanduser("~/Library/Logs")) / app_name
    else:
        log_file_dir = Path(os.path.expanduser("~/.local/state")) / app_name
    log_file_uri = log_file_dir / f"{app_name}.log"

    # 2. Add file/event log handler if not console_only
    if not console_only:
        if "win32" == sys.platform:  # pragma: no cover
            file_handler = logging.handlers.NTEventLogHandler(
                appname=app_name, logtype="Application"
            )
        else:
            if not log_file_dir.is_dir():
                try:
                    log_file_dir.mkdir(parents=True, exist_ok=True)
                except OSError as o_error:
                    print(
                        "Unable to create the logging directory "
                        f"{log_file_dir}.\n{o_error.strerror}",
                        file=sys.stderr, # Direct to stderr
                    )
                    sys.exit(1)
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file_uri, maxBytes=1048576, backupCount=5
            )
        file_handler.setFormatter(fmt=log_formatter)
        mac_logger.addHandler(file_handler)

    # 3. Add console handler if not suppressed
    if not suppress_console:
        # Check if a StreamHandler is already present to avoid duplicates
        # This is important if configure_logger might be called multiple times
        # or if other parts of the app add handlers.
        if not any(isinstance(h, logging.StreamHandler) for h in mac_logger.handlers):
            console_handler = logging.StreamHandler(stream=sys.stdout)
            console_handler.setFormatter(fmt=log_formatter)
            mac_logger.addHandler(console_handler)

    # Set the logging level
    mac_logger.setLevel(level=logging_level)
    return mac_logger


if __name__ == "__main__":  # pragma: no cover
    pass
