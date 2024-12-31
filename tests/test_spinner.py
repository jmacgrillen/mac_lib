#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        test_spinner.py
    Desscription:
        Test the console spinner.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import maclib.mac_spinner as spinner
import time


class TestSpinner():
    """
    Test the console spinner.
    """

    def test_01_default_spinner(self):
        """
        Test the default spinner is set properly.
        """
        mspinner: spinner.MacSpinner = spinner.MacSpinner()
        assert mspinner.animation_delay == 0.1
        assert mspinner.message == "Running"
        assert not mspinner.event_stop.is_set()
        assert mspinner.current_frame == 0

    def test_02_custom_spinner(self):
        """
        Test that the setting for a custom spinner are stored
        """
        custom_message: str = "This is a test."
        custom_duration: float = 1.3
        custom_spinner: spinner.MacSpinner = spinner.MacSpinner(
            initial_message=custom_message,
            animation_delay=custom_duration
        )
        assert custom_spinner.animation_delay == custom_duration
        assert custom_spinner.message == custom_message
        assert not custom_spinner.event_stop.is_set()
        assert custom_spinner.current_frame == 0

    def test_03_change_message(self):
        """
        Change the message before starting the spinner
        """
        mspinner: spinner.MacSpinner = spinner.MacSpinner()
        updated_message: str = "This message has been changed."
        mspinner.set_message(
            new_message=updated_message)
        assert mspinner.message == updated_message
        assert mspinner.animation_delay == 0.1
        assert not mspinner.event_stop.is_set()
        assert mspinner.current_frame == 0

    def test_04_test_start_stop(self):
        """
        Test the animatsion starts
        """
        mspinner: spinner.MacSpinner = spinner.MacSpinner()
        mspinner.start()
        time.sleep(1.3)
        assert mspinner.current_frame != 0
        assert not mspinner.event_stop.is_set()
        mspinner.stop()
        assert mspinner.event_stop.is_set()

    def test_06_animation_loop(self):
        """
        Test the animation loop resets.
        """
        mspinner: spinner.MacSpinner = spinner.MacSpinner()
        mspinner.current_frame = 10
        mspinner._render()
        print(len(mspinner.frames))
        assert mspinner.current_frame == 1

    def test_07_kill_spinner(self):
        """
        Test the kill handler code works
        """
        mspinner: spinner.MacSpinner = spinner.MacSpinner()
        mspinner.start()
        mspinner.kill_handler(1, 1)


if __name__ == "__main__":  # pragma: no cover
    pass
