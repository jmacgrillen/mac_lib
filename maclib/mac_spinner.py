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
import signal


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
        signal.signal(signal.SIGINT, self.kill_handler)
        self.event_stop = threading.Event()
        self.message = initial_message
        self.animation_delay = animation_delay
        self.current_frame = 0
        self.__animation_thread = threading.Thread(target=self.animate)

    def clear_line(self):
        """
        Clear the console line,
        """
        sys.stdout.write("\033[K")  # clears the line

    def _render(self) -> None:
        """
        Draw the spinner frame.
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
            self.event_stop.set()
            self.__animation_thread.join()

    def set_message(self, new_message: str) -> None:
        """
        Set the on screen message
        """
        self.message = new_message

    def kill_handler(self, signum: int, frame: any) -> None:
        """
        Capture CTRL+C and kill the animation
        """
        self.stop()
        time.sleep(1)
        self.clear_line()


if __name__ == "__main__":  # pragma: no cover
    pass
