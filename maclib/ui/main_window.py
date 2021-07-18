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

import os
import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from maclib.ui.status_bar import MacStatusBar
from maclib.mac_detect import MacDetect

class MacWindow(tk.Toplevel):
    """
    Base window for mac_lib ui
    """
    parent:tk.Tk
    main_content:ttk.Frame
    status_bar:MacStatusBar
    menu_bar:tk.Menu
    mac_detect: MacDetect = MacDetect()
    style: ThemedStyle 

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
        self.parent.geometry("800x600")
        self.withdraw()
        # When the window is closed, kill the program.
        self.protocol(
            "WM_DELETE_WINDOW",
            self.parent.destroy)
        self.parent.config
        self.parent.grid_rowconfigure(index=0, weight=1)
        self.parent.grid_columnconfigure(index=0, weight=1)
        self.main_content = ttk.Frame(master=self.parent)
        self.main_content.grid(row=0, column=0, sticky='nswe')
        self.main_content.grid_rowconfigure(index=0, weight=1)
        self.main_content.grid_columnconfigure(index=0, weight=1)
        self.main_content.grid_propagate(True)
        this_file = os.path.realpath(__file__)
        this_directory = os.path.dirname(this_file)
        if self.mac_detect.os_theme == "Dark":
            style = ThemedStyle(self.parent)
            azure_dark_file = os.path.join(this_directory, "theme/azure-dark.tcl")
            self.parent.tk.call("source", azure_dark_file)
            style.theme_use(theme_name="azure-dark")
        else:
            style = ThemedStyle(self.parent)
            azure_file = os.path.join(this_directory, "theme/azure.tcl")
            self.parent.tk.call("source", azure_file)
            style.theme_use(theme_name="azure")

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
        self.menu_bar = tk.Menu(master=self.parent) # , relief=FLAT)
        self.parent.configure(menu=self.menu_bar)


if __name__ == "__main__":
    pass
