#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        filter_list.py
    Desscription:
        A filter list box for mac_lib/ui.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import tkinter as tk
import tkinter.ttk as ttk

class MacFilterListBox(tk.Frame):
    """
    Create a list box with a filter box at the top.
    """
    __list_box:tk.Listbox
    __filter_box:ttk.Entry
    __scroll_bar:ttk.Scrollbar
    __main_list: list = []
    __box_list: list = []
    __filter_text:tk.StringVar


    def __init__(self, parent:tk.Misc, data_list:list, *args, **kwargs):
        """
        Create the filtered list box.
        """
        super(MacFilterListBox, self).__init__(parent, *args, **kwargs)
        self.pack(fill='y', expand=True)
        self.__filter_text = tk.StringVar()
        self.__filter_text.trace("w", self._update_list)
        self.__filter_box = ttk.Entry(self, textvariable=self.__filter_text)
        self.__filter_box.grid(row=0, sticky='n')
        self.__list_box = tk.Listbox(self, width=100)
        self.__list_box.grid(row=1)
        self.__main_list = data_list

    def _update_list(self, *args):
        """
        Update the displayed list based on what has been typed
        """
    
