#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_events.py
    Desscription:
        A simple Observer pattern implementation. This
        is not complicated,but is multithreaded.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
import logginkg
from maclib.mac_exception import MacException
from maclib.mac_logger import LOGGER_NAME
from dataclasses import dataclass, field
from threading import Lock


class MacEventException(MacException):
    pass


@dataclass
class MacEvent(object):
    """
    Event is base class providing an interface for all subsequent
    (inherited) events.
    """
    event_action: str
    event_info: dict = field(default_factory=dict)


class MacEventPublisher(object):
    """
    The Publisher class.
    """
    subscribers: dict
    valid_events: list
    __lock: Lock
    m_logger: logging.Logger

    def __init__(self, valid_events: list):
        self.subscribers = dict()
        self.valid_events = valid_events
        self.__lock = Lock()
        self.m_logger = logging.getLogger(LOGGER_NAME)
        with self.__lock:
            for valid_event in valid_events:
                self.subscribers[valid_event] = list()

    def register(self, event_action: str, subscriber_callabck) -> None:
        """
        Register a subscriber for a given event.
        """
        with self.__lock:
            if event_action in self.subscribers.keys():
                self.subscribers[event_action].append(subscriber_callabck)
                self.m_logger.debug(f"Function {subscriber_callabck} has been"
                                    " registered against event "
                                    f"{event_action}.")
            else:
                raise MacEventException(
                    str_message=f"The event type {event_action} is not a "
                                "valid type.")

    def unregister(self, event_action: str, subscriber_callabck) -> None:
        """
        Unregister a subscriber for a given event.
        """
        with self.__lock:
            if event_action in self.subscribers.keys():
                if subscriber_callabck in self.subscribers[event_action]:
                    self.subscribers[event_action].remove(subscriber_callabck)

    def post_event(self, event: MacEvent) -> None:
        """
        Dispatch an event to its subscriber.
        """
        with self.__lock:
            if event.event_action in self.subscribers.keys():
                for subscriber in self.subscribers[event.event_action]:
                    self.m_logger.debug(f"Posting event {event.event_action} "
                                        f"to subscriber {subscriber}.")
                    subscriber(event)
            else:
                raise MacEventException(
                    str_message=f"The event type {event.event_action} "
                                f"specified in the event {event} is not a "
                                "valid type for this publisher.")


if __name__ == "__main__":  # pragma: no cover
    pass
