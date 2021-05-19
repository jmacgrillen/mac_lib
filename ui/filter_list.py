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
import typing

class MacFilterListBox(tk.Frame):
    """
    Create a list box with a filter box at the top.
    """
    __list_box:tk.Listbox
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
        self.pack(fill='y', expand=True)
        self.__filter_text = tk.StringVar()
        self.__filter_text.trace("w", self.update_list_box)
        self.__filter_box = ttk.Entry(self, textvariable=self.__filter_text, width=width)
        self.__filter_box.grid(row=0, sticky='n')
        self.__list_box = tk.Listbox(self, width=width)
        self.__list_box.grid(row=1,column=0)
        self.__list_box.bind('<<ListboxSelect>>', self.on_select)
        self.selected_value = ""
        self.selected_index = -1
        self.__scroll_bar = ttk.Scrollbar(self, orient='vertical')
        self.__scroll_bar.grid(row=1,column=1, sticky='ns')
        self.__list_box.config(yscrollcommand=self.__scroll_bar.set)
        self.__scroll_bar.config(command=self.__list_box.yview)
        self.__main_list = data_list
        self.update_list_box()

    def update_list_box(self, *args) -> None:
        """
        Update the displayed list based on what has been typed
        """
        self.__list_box.selection_clear(0, tk.END)
        search_term = self.__filter_box.get()

        self.__list_box.delete(0, tk.END)
        self.__displayed_items_index.clear()

        for index, item in enumerate(self.__main_list, start=0):
            if search_term.lower() in item.lower():
                self.__list_box.insert(tk.END, item)
                self.__displayed_items_index.append(index)

    def on_select(self, event:tk.Event) -> None:
        """
        Record the item that has been selected.
        """
        event_widget = event.widget
        self.selected_value = ""
        self.selected_index = -1
        if event_widget.curselection():
            index = int(event_widget.curselection()[0])
            self.selected_value = event_widget.get(index)
            self.selected_index = self.__displayed_items_index[index]
            if '_MacFilterListBox__bound_call_back' in vars(self):
                self.__bound_call_back(selected_value=self.selected_value,
                                       selected_index=self.selected_index)

    def bind(self, call_back:typing.Callable) -> None:
        """
        Store the callback function used when a selection has been made.
        """
        self.__bound_call_back = call_back


if __name__ == "__main__":
    pass