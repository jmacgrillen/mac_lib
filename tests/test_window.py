#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        test_window.py
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
from src.ui.main_window import MacWindow
from src.ui.filter_list import MacFilterListBox

def donothing():
   x = 0

def do_something(**kwargs):
    print(kwargs['selected_value'])

main_app = tk.Tk()
main_app.title("MacTest")
main_window = MacWindow(parent=main_app)
main_window.add_status_bar("Ready Player 1")
main_window.add_menu_bar()
filemenu = tk.Menu(main_window.menu_bar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=main_app.quit)
main_window.menu_bar.add_cascade(label="File", menu=filemenu)


test_list = ["t1", "t2", "t3", "m1", "m2", "m3", "o1", "o2", "o3",
             "a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
f_list = MacFilterListBox(parent=main_window.main_content, 
                          data_list=test_list)
f_list.bind(do_something)

main_window.mainloop()
