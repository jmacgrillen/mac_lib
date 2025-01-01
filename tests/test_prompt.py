#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        test_prompt.py
    Desscription:
        Test the simple event system.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import pytest
import maclib.mac_prompt as mprompt


def test_01_test_prompt_default_value_mistake(monkeypatch):
    """

    """
    with pytest.raises(ValueError):
        mprompt.prompt_yes_no("test", "maybe")


def test_02_test_prompt_default_value_true(monkeypatch):
    """

    """
    monkeypatch.setattr('builtins.input', lambda: 'y')
    test = mprompt.prompt_yes_no("test", "yes")
    assert test is True


def test_03_test_prompt_default_value_false(monkeypatch):
    """

    """
    monkeypatch.setattr('builtins.input', lambda: 'n')
    test = mprompt.prompt_yes_no("test", "no")
    assert test is False


def test_04_test_prompt_default_value_none(monkeypatch):
    """

    """
    monkeypatch.setattr('builtins.input', lambda: 'n')
    test = mprompt.prompt_yes_no("test")
    assert test is False


def test_05_wrong_input_then_right_one(monkeypatch, capfd):
    """

    """
    inputs = iter(['maybe', 'yes'])

    monkeypatch.setattr('builtins.input', lambda: next(inputs))
    test = mprompt.prompt_yes_no("test")
    captured = capfd.readouterr()
    assert captured.out.find("Please respond with 'yes' or 'no'") != -1
    assert test is True


def test_06_test_prompt_default_value(monkeypatch):
    """

    """
    monkeypatch.setattr('builtins.input', lambda: '')
    test = mprompt.prompt_yes_no("test", "no")
    assert test is False


if __name__ == "__main__":
    pass
