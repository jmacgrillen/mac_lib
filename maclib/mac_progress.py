#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_progress.py
    Desscription:
        This is very heavily based on this gist
        https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
        Originally released under the MIT License.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import sys


def progress(count, total, status=''):
    """
    Console based progress bar.
    """
    bar_len = 55
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 2)
    str_precents = f" {percents:>5}% "
    bar = '▓' * filled_len + '░' * (bar_len - filled_len)
    full_bar = bar[:int(bar_len / 2)] + str_precents + bar[int(bar_len / 2):]

    fmt_str = f'[{full_bar}] {status}'
    print('\b' * len(fmt_str), end='')  # clears the line
    sys.stdout.write(fmt_str)
    sys.stdout.flush()
    return percents
