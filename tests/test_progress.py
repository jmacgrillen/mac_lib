#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        test_progress.py
    Desscription:
        Test the progress bar.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import maclib.mac_progress as pbar


def test_progress_bar():
    """
    Test the progress bar
    """
    max_size: int = 100
    for i in range(max_size):
        output = pbar.progress(i, max_size, "Big job")
        assert output == i
