#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_spinner.py
    Description:
        Lightweight console bassed spinner.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import sys
import threading
import time
import signal


class MacSpinner(object):
    """
    A simple lightweight console spinner

    Attributes:
        message (str):
            The message to be displayed.
        current_frame (int):
            The current animation frame of the spinner.
        __animation_thread (threading.Thread):
            The thread that runs the spinner animation.
        event_stop (threading.Event):
            The event that stops the spinner.
        frames (list):
            The frames of the spinner that will be animated.

    Methods:
        __init__:
            Initialise the spinner.
        clear_line:
            Clear the console line.
        _render:
            Draw the spinner frame.
        animate:
            Animate the spinner.
        start:
            Start the spinner.
        stop:
            Stop the spinner.
        set_message:
            Set the message to be displayed.
        kill_handler:
            Capture CTRL+C and kill the animation.
    """
    message: str
    current_frame: int
    __animation_thread: threading.Thread
    event_stop: threading.Event
    frames = [
        '⠋',
        '⠙',
        '⠹',
        '⠸',
        '⠼',
        '⠴',
        '⠦',
        '⠧',
        '⠇',
        '⠏'
    ]

    def __init__(self,
                 initial_message: str = "Running",
                 animation_delay: float = 0.1) -> None:
        """
        Initiaise all the variables needed to make this work.
        """
        super(MacSpinner, self).__init__()
        signal.signal(signal.SIGINT, self.kill_handler)
        self.event_stop = threading.Event()
        self.message = initial_message
        self.animation_delay = animation_delay
        self.current_frame = 0
        self.__animation_thread = threading.Thread(target=self.animate)

    def clear_line(self):
        """
        Clear the console line.

        Args:
            None

        Return:
            None
        """
        sys.stdout.write("\033[K")  # clears the line

    def _render(self) -> None:
        """
        Draw the spinner frame.

        Args:
            None

        Return:
            None
        """
        if self.current_frame == len(self.frames):
            self.current_frame = 0
        out_string = f"{self.frames[self.current_frame]}" \
                     f" {self.message}\r"
        self.clear_line()
        sys.stdout.write(out_string)
        sys.stdout.flush()
        if self.current_frame < len(self.frames):
            self.current_frame += 1

    def animate(self) -> None:
        """
        Animate the spinner

        Args:
            None

        Return:
            None
        """
        while not self.event_stop.is_set():
            self._render()
            time.sleep(self.animation_delay)

    def start(self) -> None:
        """
        Start the spinner.

        Args:
            None

        Return:
            None
        """
        self.__animation_thread.start()

    def stop(self) -> None:
        """
        Stop the spinner

        Args:
            None

        Return:
            None
        """
        if not self.event_stop.is_set():
            self.event_stop.set()
            self.__animation_thread.join()

    def set_message(self, new_message: str) -> None:
        """
        Set the on screen message

        Args:
            new_message (str):
                The message to be displayed at the front.

        Return:
            None
        """
        self.message = new_message

    def kill_handler(self, signum: int, frame: any) -> None:
        """
        Capture CTRL+C and kill the animation

        Args:
            signum (int):
                The signal number recieved.
            frame (any):
                Pass

        Return:
            None
        """
        self.stop()
        time.sleep(1)
        self.clear_line()


if __name__ == "__main__":  # pragma: no cover
    pass
