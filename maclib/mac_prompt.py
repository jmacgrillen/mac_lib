#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_prompt.py
    Desscription:
        Handle a yes/no user prompt.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import sys


def prompt_yes_no(question: str, default: str = "no") -> bool:
    """
    Ask the user a yes/no question via raw_input() and return a boolean
    depending on whether they answer yes (True) or no (False).

    Args:
        question (str): A string that is presented to the user.
        default (str): If the user just hits enter, this is the default we want
                       this funtion to process

    Returns:
        bool: Returns True if user answers yes, or False if user answers no.
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    match default:
        case "yes" | "y":
            prompt = " [Y/n] "
        case "no" | "n":
            prompt = " [y/N] "
        case _:
            raise ValueError("Invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n"
            )
