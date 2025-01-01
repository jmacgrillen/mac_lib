#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        test_events.py
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
import maclib.mac_events as mevents


def test_01_test_mac_event_exception_gets_raised(monkeypatch):
    """

    """
    valid_events = ["event1", "event2", "event3"]

    def my_callback(event):
        """
        A simple callback.
        """
        pass

    test_events = mevents.MacEventPublisher(valid_events=valid_events)
    with pytest.raises(mevents.MacEventException):
        test_events.register("event4", my_callback)


def test_02_test_post_event_exception1_gets_raised(monkeypatch):
    """

    """
    valid_events = ["event1", "event2", "event3"]

    test_event = mevents.MacEvent(event_action="event1",
                                  event_info={'app_name': 'test_app'})

    def my_callback():
        """
        A simple callback.
        """
        pass

    test_events = mevents.MacEventPublisher(valid_events=valid_events)
    test_events.register("event1", my_callback)
    with pytest.raises(mevents.MacEventException):
        test_events.post_event(test_event)


def test_03_test_post_event_exception2_gets_raised(monkeypatch):
    """

    """
    valid_events = ["event1", "event2", "event3"]

    test_event = mevents.MacEvent(event_action="event4",
                                  event_info={'app_name': 'test_app'})

    def my_callback(event):
        """
        A simple callback.
        """
        pass

    test_events = mevents.MacEventPublisher(valid_events=valid_events)
    test_events.register("event1", my_callback)
    with pytest.raises(mevents.MacEventException):
        test_events.post_event(test_event)


if __name__ == "__main__":
    pass
