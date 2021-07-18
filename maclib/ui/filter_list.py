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
from tkinter import ttk
import typing

class MacFilterListBox(tk.Frame):
    """
    Create a list box with a filter box at the top.
    """
    __list_box: ttk.Treeview    # tk.Listbox
    __filter_box:ttk.Entry
    __scroll_bar:ttk.Scrollbar
    __main_list:list = []
    __filter_text:tk.StringVar
    __displayed_items_index:list = []
    __bound_call_back:typing.Callable
    # Check these values to see what the user has selected.
    # If the index is -1, and the value is an empty string, then 
    # the user hasn't selected anything
    selected_value:str
    selected_index:int

    def __init__(self, parent:tk.Misc, data_list:list, width:int=50, *args, **kwargs):
        """
        Create the filtered list box.
        """
        super(MacFilterListBox, self).__init__(parent, *args, **kwargs)
        self.grid(row=0, column=0, sticky='ns', padx=5.0, pady=2.0)
        self.grid_propagate(True)
        self.__filter_text = tk.StringVar()
        self.__filter_text.trace(mode="w", callback=self.update_list_box)
        self.__filter_box = ttk.Entry(self,
                                      textvariable=self.__filter_text,
                                      width=width)
        self.__filter_box.grid(row=0, sticky='n')
        self.__list_box = ttk.Treeview(master=self, show='tree', columns="1")
        self.__list_box.column("#0",minwidth=width,width=width, stretch=False)
        self.__list_box.grid(row=1,column=0, sticky='ns')
        self.__list_box.bind(sequence='<ButtonRelease-1>', func=self.on_select)
        self.selected_value = ""
        self.selected_index = -1
        self.__scroll_bar = ttk.Scrollbar(self, orient='vertical')
        self.__scroll_bar.grid(row=1,column=1, sticky='ns')
        self.__list_box.config(yscrollcommand=self.__scroll_bar.set)
        self.__scroll_bar.config(command=self.__list_box.yview)
        self.__main_list = data_list
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)
        self.update_list_box()

    def update_list_box(self, *args) -> None:
        """
        Update the displayed list based on what has been typed
        """
        search_term = self.__filter_box.get()
        self.__list_box.delete(*self.__list_box.get_children())
        self.__displayed_items_index.clear()

        for index, item in enumerate(iterable=self.__main_list, start=0):
            if search_term.lower() in item.lower():
                self.__list_box.insert(
                    index=index,
                    parent= '',
                    text=item)
                self.__displayed_items_index.append(index)

    def on_select(self, event:tk.Event) -> None:
        """
        Record the item that has been selected.
        """
        iindex = event.widget.selection()
        index = int(iindex[0][1:], 16)
        self.selected_value = str(event.widget.item(iindex)['text'])
        self.selected_index = index
        
        if '_MacFilterListBox__bound_call_back' in vars(self):
            self.__bound_call_back(selected_value=self.selected_value,
                                   selected_index=self.selected_index)

    def bind(self, call_back:typing.Callable) -> None:
        """
        Store the callback function used when a selection has been made.
        """
        self.__bound_call_back = call_back

    def set_main_list(self, new_list: list) -> None:
        """
        Update the main list
        """
        if new_list:
            self.__main_list = new_list
            self.update_list_box()

if __name__ == "__main__":
    pass