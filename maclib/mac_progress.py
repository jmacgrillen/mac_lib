#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_progress.py
    Description:
        This is very heavily based on this gist
        https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
        Originally released under the MIT License.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import sys


def progress(count: any, total: any, status: str = '') -> float:
    """
    Console based progress bar.

    Args:
        count (any):
            The current progress.
        total (any):
            The total number that represents 100% complete.
        status (str):
            The status message to display.

    Return:
        float:
            The percentage complete.
    """
    bar_len: int = 55
    filled_len: int = int(round(bar_len * count / float(total)))

    percents: float = round(100.0 * count / float(total), 2)
    str_precents: str = f" {percents:>5}% "
    bar: str = '▓' * filled_len + '░' * (bar_len - filled_len)
    full_bar: str = bar[:int(bar_len / 2)] + str_precents + bar[
        int(bar_len / 2):]

    fmt_str: str = f'[{full_bar}] {status}'
    print('\b' * len(fmt_str), end='')  # clears the line
    sys.stdout.write(fmt_str)
    sys.stdout.flush()
    return percents


if __name__ == "__main__":  # pragma: no cover
    pass
