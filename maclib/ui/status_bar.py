#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        status_bar.py
    Desscription:
        a Status bar for the main window in mac_lib/ui.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import tkinter as tk
import tkinter.ttk as ttk

class MacStatusBar(tk.Frame):
    """
    tkInter statusbar for a window
    """
    parent:ttk.Frame
    status_bar:ttk.Label
    size_grip:ttk.Sizegrip
    status_text:tk.StringVar

    def __init__(self, 
                 parent:ttk.Frame,
                 default_text:str="Ready",
                 *args,
                 **kwargs):
        """
        Initialise the status bar.
        """
        super(MacStatusBar, self).__init__(*args, **kwargs)
        self.parent = parent
        self.grid(row=2, column=0,
                  sticky='wse', padx=3, pady=2)
        self.grid_propagate(True)
        self.status_text = tk.StringVar()
        self.status_text.set(default_text)
        self.status_bar = ttk.Label(master=self,
                                    textvariable=self.status_text,
                                    anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky='we')
        self.size_grip = ttk.Sizegrip(self)
        self.size_grip.grid(row=1, column=4, sticky='se')
        self.columnconfigure(0, weight=1)

    def set_text(self, new_text:str):
        """
        Change the text on display on the status bar.
        """
        self.status_text.set(new_text)

if __name__ == "__main__":
    pass
