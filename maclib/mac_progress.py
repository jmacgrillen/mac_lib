#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name:
    mac_progress.py
Description:
    A console-based progress bar.
Version:
    1 - Initial release (Class-based)
Author:
    J.MacGrillen <macgrillen@gmail.com>
Copyright:
    Copyright (c) John MacGrillen. All rights reserved.
"""
import sys
import threading
import time
from typing import Optional


class MacProgressBar(object):
    """
    A simple console-based progress bar.

    Attributes:
        total (int):
            The total value that represents 100% completion.
        bar_len (int):
            The fixed length of the progress bar in characters.
        message (str):
            The status message to display alongside the bar.
        __lock (threading.Lock):
            A lock to ensure thread-safe printing to the console.
        __current_progress (int):
            The current progress count.
        __is_active (bool):
            Flag to indicate if the progress bar is currently active.

    Methods:
        __init__:
            Initialise the progress bar.
        _clear_line:
            Clear the current console line.
        update:
            Update the progress bar with a new count and optional message.
        finish:
            Complete the progress bar and clear the line.
    """

    def __init__(
        self, total: int, message: str = "", bar_len: int = 50
    ) -> None:
        """
        Initialize the progress bar.

        Args:
            total (int):
                The total value that represents 100% completion.
            message (str):
                An initial status message to display. Defaults to an empty string.
            bar_len (int):
                The fixed length of the progress bar in characters. Defaults to 50.
        """
        super().__init__()
        if not isinstance(total, int) or total < 0:
            raise ValueError("Total must be a non-negative integer.")
        if total == 0:
            self.total = 1  # Avoid ZeroDivisionError, treat as 100% complete if total is 0
        else:
            self.total = total

        self.bar_len = bar_len
        self.message = message
        self.__lock = threading.Lock()
        self.__current_progress = 0
        self.__is_active = False

        # Initial render to show the bar immediately
        self.update(0, message)

    def _clear_line(self) -> None:
        """
        Clears the current console line using ANSI escape codes.
        """
        sys.stdout.write(
            "\r\033[K"
        )  # Carriage return + clear line from cursor to end

    def update(self, count: int, message: Optional[str] = None) -> None:
        """
        Update the progress bar with the current count and an optional message.

        Args:
            count (int):
                The current progress count.
            message (Optional[str]):
                An optional new status message to display. If None, the existing
                message is retained.
        """
        with self.__lock:
            if message is not None:
                self.message = message

            # Ensure count is within valid bounds
            self.__current_progress = max(0, min(count, self.total))

            filled_len = int(
                round(
                    self.bar_len * self.__current_progress / float(self.total)
                )
            )
            percents = round(
                100.0 * self.__current_progress / float(self.total), 2
            )

            # Format percentage string, right-aligned with 5 characters, 2 decimal places
            str_percents = f"{percents:5.2f}%"

            # Construct the filled and empty parts of the bar
            bar_filled = "▓" * filled_len
            bar_empty = "░" * (self.bar_len - filled_len)

            # Combine bar and percentage, placing percentage in the middle
            # This logic is kept similar to your original for consistency,
            # but can be adjusted if you prefer percentage outside the bar.
            # Calculate where to split the bar for percentage insertion
            half_bar_len = self.bar_len // 2
            bar_with_percent = f"{bar_filled}{bar_empty}"

            # If the percentage string is longer than the bar, or if it doesn't fit neatly,
            # place it outside the bar for simplicity.
            if (
                len(str_percents) > self.bar_len
                or filled_len < len(str_percents) / 2
                or (self.bar_len - filled_len) < len(str_percents) / 2
            ):
                display_bar = f"[{bar_filled}{bar_empty}] {str_percents} "
            else:
                # Attempt to insert into the bar if enough space
                insert_pos = filled_len - (len(str_percents) // 2)
                if (
                    insert_pos < 0
                ):  # Adjust if percentage string starts before the bar
                    insert_pos = 0

                # Ensure the end of the percentage string doesn't go past the bar length
                end_pos = insert_pos + len(str_percents)
                if end_pos > self.bar_len:
                    insert_pos = self.bar_len - len(str_percents)
                    if insert_pos < 0:
                        insert_pos = 0  # Fallback if still too long

                bar_parts = list(f"{bar_filled}{bar_empty}")
                for i, char in enumerate(str_percents):
                    if insert_pos + i < self.bar_len:
                        bar_parts[insert_pos + i] = char
                display_bar = f"[{''.join(bar_parts)}]"

            # Final output string
            fmt_str = f"{display_bar} {self.message}"

            self._clear_line()
            sys.stdout.write(fmt_str)
            sys.stdout.flush()
            self.__is_active = True

    def finish(self, final_message: Optional[str] = None) -> None:
        """
        Completes the progress bar, sets it to 100%, and clears the line.

        Args:
            final_message (Optional[str]):
                An optional final message to display before clearing.
        """
        if self.__is_active:
            self.update(self.total, final_message or "Complete")
            sys.stdout.write("\n")  # Move to the next line after completion
            sys.stdout.flush()
            self.__is_active = False


if __name__ == "__main__":
    pass
