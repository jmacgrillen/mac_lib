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
from ui.status_bar import MacStatusBar


class MacWindow(tk.Toplevel):
    """
    Base window for mac_lib ui
    """
    parent:tk.Tk
    main_content:ttk.Frame
    status_bar:MacStatusBar
    menu_bar:tk.Menu

    def __init__(self, 
                 parent:tk.Tk,
                 window_icon:object=None,
                 *args,
                 **kwargs):
        """
        Create a tk window
        """
        super(MacWindow, self).__init__(*args, **kwargs)
        self.parent = parent
        self.parent.geometry("1024x768")
        self.withdraw()
        # When the window is closed, kill the program.
        self.protocol(
            "WM_DELETE_WINDOW",
            self.parent.destroy)
        self.main_content = ttk.Frame(self.parent)
        self.main_content.pack(fill='both', expand=True)
        
        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

    def add_status_bar(self, default_text:str="Ready"):
        """
        Add a status bar to the main window
        """
        self.status_bar = MacStatusBar(parent=self.main_content,
                                       default_text=default_text)

    def add_menu_bar(self):
        """
        Most apps need a menu bar. May as well connect it to the window.
        """
        self.menu_bar = tk.Menu(master=self.parent)
        self.parent.configure(menu=self.menu_bar)



if __name__ == "__main__":
    pass
