# mac_lib

[![Python](https://img.shields.io/badge/python-3-green.svg)](https://www.python.org/downloads/release/python-383/)
[![GitHub license](https://img.shields.io/github/license/jmacgrillen/mac_lib.svg)](https://github.com/jmacgrillen/mac_lib/blob/main/LICENSE)

mac_lib is a collection of handy Python boiler plate code snippets.

These are dsigned to help *me* accelerate creating Python programs with out-of-the-box support for logging, settingss files, etc.

The code includes:
- `mac_colours.py` - Nothing earth shattering, just rgb to hex conversion
- `mac_detect.py` - A few pieces to help identify bits like OS and Python version
- `mac_exception.py` - A simple exception that logs the error message into the application log
- `mac_file_management.py` - Some routines to help me with file management
- `mac_logger.py` - Configures the builtin logging so it logs to file and console in an easy to understand way
- `mac_progress.py` - A simple console based progress bar
- `mac_request.py` - Small wrapper around *requests* mostly to handle persistent headers
- `mac_settings.py` - Application settings, built on the Singleton pattern
- `mac_single.py` - Singleton pattern class
- `mac_spinner.py` - A simple console spinner