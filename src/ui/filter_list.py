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
    __filter_text:tk.StringVar
    # List of the index number of the items
    # being displayed from the main list.
    displayed_items_index: list = []


    def __init__(self, parent:tk.Misc, data_list:list, width:int, *args, **kwargs):
        """
        Create the filtered list box.
        """
        super(MacFilterListBox, self).__init__(parent, *args, **kwargs)
        self.pack(fill='y', expand=True)
        self.__filter_text = tk.StringVar()
        self.__filter_text.trace("w", self.update_list_box)
        self.__filter_box = ttk.Entry(self, textvariable=self.__filter_text, width=width)
        self.__filter_box.grid(row=0, sticky='n')
        self.__list_box = tk.Listbox(self, width=width)
        self.__list_box.grid(row=1,column=0)
        self.__scroll_bar = ttk.Scrollbar(self, orient='vertical')
        self.__scroll_bar.grid(row=1,column=1, sticky='ns')
        self.__list_box.config(yscrollcommand=self.__scroll_bar.set)
        self.__scroll_bar.config(command=self.__list_box.yview)
        self.__main_list = data_list
        self.update_list_box()

    def update_list_box(self, *args):
        """
        Update the displayed list based on what has been typed
        """
        search_term = self.__filter_box.get()

        self.__list_box.delete(0, tk.END)
        self.displayed_items_index.clear()

        for index, item in enumerate(self.__main_list, start=0):
            if search_term.lower() in item.lower():
                self.__list_box.insert(tk.END, item)
                self.displayed_items_index.append(index)
