#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_spinner.py
    Desscription:
        Lightweight console bassed spinner.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import sys
import threading
import time


class MacSpinner(object):
    """
    A simple lightweight console spinner
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
        self.__animation_thread = threading.Thread(target=self.animate)
        self.event_stop = threading.Event()
        self.message = initial_message
        self.animation_delay = animation_delay
        self.current_frame = 0

    def _render(self) -> None:
        """
        Draw the spinner frame.
        """
        if self.current_frame == len(self.frames):
            self.current_frame = 0
        out_string = f"{self.frames[self.current_frame]}" \
            f" {self.message}\r"
        sys.stdout.write("\033[K")  # clears the line
        sys.stdout.write(out_string)
        sys.stdout.flush()
        if self.current_frame < len(self.frames):
            self.current_frame += 1

    def animate(self):
        """
        Animate the spinner
        """
        while not self.event_stop.is_set():
            self._render()
            time.sleep(self.animation_delay)

    def start(self) -> None:
        """
        Start the spinner.
        """
        self.__animation_thread.start()

    def stop(self) -> None:
        """
        Stop the spinner
        """
        if not self.event_stop.is_set():
            time.sleep(1)
            self.event_stop.set()

    def set_message(self, new_message: str) -> None:
        """
        Set the on screen message
        """
        self.message = new_message


if __name__ == "__main__":  # pragma: no cover
    pass
