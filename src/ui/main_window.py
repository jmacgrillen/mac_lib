#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_window.py
    Desscription:
        The main window for mac_lib/ui.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import tkinter as tk
import tkinter.ttk as ttk


class MacWindow(tk.Toplevel):
    """
    Base window for mac_lib ui
    """
    window: tk.Tk = None
    status_bar: ttk.Label = None
    resize_grip: ttk.Label = None
    master:object = None
    mouse_x: int = None
    mouse_y: int = None

    def __init__(
        self, master:object,
        window_title:str,
        window_icon:object=None,
        *args,
        **kwargs):
        """
        Create a tk window
        """
        super(MacWindow, self).__init__(args, kwargs)
        self.master = master
        self.title(window_title)
        # When the window is closed, kill the program.
        self.protocol(
            "WM_DELETE_WINDOW",
            self.master.destroy)

    def add_status_bar(self, default_text:str="Ready") -> None:
        """
        Add a status bar to the window
        """
        # Now create the resize grip on the window
        self.status_bar = ttk.Label(
            master=self,
            text=default_text,
            anchor=tk.W)
        self.resize_grip = ttk.Label(
            master=self.status_bar,
            text="...",
            background="gray50",
            cursor="sizing")
        self.resize_grip.pack(
            side=tk.RIGHT,
            fill=tk.BOTH)
        self.status_bar.pack(
            side=tk.BOTTOM,
            fill=tk.X)
        self.resize_grip.bind(
            sequence="<Button-1>",
            func=self.grip_active)
        self.resize_grip.bind(
            sequence="<ButtonRelease-1>",
            func=self.grip_release)
        self.resize_grip.bind(
            sequence="<B1-Motion>",
            func=self.resize_window)

    def grip_active(self, event: tk.Event) -> None:
        """
        Main mouse button clicked.
        """
        self.mouse_x = event.x
        self.mouse_y = event.y

    def grip_release(self, event: tk.Event) -> None:
        """
        Main mouse button released
        """
        self.mouse_x = None
        self.mouse_y = None

    def resize_window(self, event: tk.Event) -> None:
        """
        Mouse has been moved with the main mouse button down.
        """
        delta_x = event.x - self.mouse_x
        delta_y = event.y - self.mouse_y
        new_x = self.winfo_width() + delta_x
        new_y = self.winfo_height() + delta_y
        self.geometry("{0}x{1}".format(
            new_x, new_y))


t_app = tk.Tk()
t_app.withdraw()
style = ttk.Style(master=t_app)
style.theme_use('xpnative')
print(style.theme_names())
t_window = MacWindow(t_app, "MacTest")
t_app._toplevel = t_window
t_window.add_status_bar()
t_app.mainloop()
