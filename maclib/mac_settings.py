#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_settigs.py
    Desscription:
        Manage applicatuon settings from a YAML file.
        There should be a set of defaults.
    Version:
        5 - Switched to event messages from direct callback.
        4 - Added callback support to notify objects of settings changes.
        3 - Added a file watcher to pickup when the settings are
            changed by another process.
        2 - Settings are now automatically created where they
            should be based on the platform the program is running
            on. No longer need to remember where they should be.
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""
from typing import Optional, Any
from functools import reduce
import operator
import logging
import yaml
import shutil
import pathlib
import os
import sys
import copy
from threading import Lock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import maclib.mac_file_management as file_m
import maclib.mac_logger as mac_logger
from maclib.mac_single import MacSingleInstance
from maclib.mac_exception import MacException
from maclib.mac_events import MacEventPublisher, MacEvent


def dict_diff(dict_a: dict, dict_b: dict) -> dict:
    """
    Return the difference between two dictionaries.

    Args:
        dict_a (dict):
            The first dictionary to compare against.
        dict_b (dict):
            The second dictionary to compare against.

    Return:
        dict:
            A dictionary showing what has been added, removed, or changed
            between dict_a and dict_b.  
    """
    changes: dict = {}
    changes["added"] = {k: dict_b[k] for k in dict_b.keys() - dict_a.keys()}
    changes["removed"] = {k: dict_a[k] for k in dict_a.keys() - dict_b.keys()}
    common_keys = dict_a.keys() & dict_b.keys()
    changes["changed"] = {
        k: (dict_a[k], dict_b[k])
        for k in common_keys
        if dict_a[k] != dict_b[k]
    }
    return changes


class MacSettingsException(MacException):
    """
    Exception from MacSettings.
    """

    pass


class MacSettingsWatchdogHandler(FileSystemEventHandler):
    """
    Set a watcher on the settings file, so we can check
    whether there have been changes made. If there is then
    we reload the settings.
    """

    mac_logger: logging.Logger
    _pause_observer: bool = False
    events_publisher: MacEventPublisher
    events = [
        "reload_settings_file",
        "settings_file_created",
        "settings_file_deleted",
    ]

    def __init__(self):
        """
        Store the main settings object
        """
        super(MacSettingsWatchdogHandler).__init__()
        self.mac_logger = logging.getLogger(mac_logger.LOGGER_NAME)
        self.events_publisher = MacEventPublisher(self.events)

    def on_modified(self, event) -> None:
        """
        We're only interested in whether the file has been changed or not.
        Send the reload event to the registered class(es).

        Args:
            event (_type_):
                The file change event.

        Return:
            None
        """
        if not self._pause_observer:
            self.mac_logger.debug("File change detected.")
            update_event = MacEvent(event_action=self.events[0])
            self.events_publisher.post_event(event=update_event)

    def on_created(self, event) -> None:
        """
        Register whether the file has been created or not.

        Args:
            event (_type_):
                The file ceate event.

        Return:
            None
        """
        if not self._pause_observer:
            self.mac_logger.debug("File created detected")
            create_event = MacEvent(event_action=self.events[1])
            self.events_publisher.post_event(event=create_event)

    def on_delete(self, event) -> None:
        """
        Register when the file has been deleted

        Args:
            event (_type_):
                The file delete event.

        Return:
            None
        """
        if not self._pause_observer:
            self.mac_logger.debug("File delete detected")
            delete_event = MacEvent(event_action=self.events[2])
            self.events_publisher.post_event(event=delete_event)


class MacSettings(metaclass=MacSingleInstance):
    """
    Handle global apps setting using a singleton class.
    Make sure the logger is initialised before calling this class.
    """

    mac_logger: logging.Logger
    settings_file_directory: str
    settings_file_path: str
    default_settings_path: str
    events_publisher: MacEventPublisher
    __settings_file_observer: Observer
    __file_change_handler: MacSettingsWatchdogHandler
    __app_settings: dict
    __thread_lock: Lock
    events = ["settings_change", "settings_loaded"]

    def __init__(self, app_name: str, default_settings_path: str) -> None:
        """
        Initialise the settings singleton.

        Args:
            app_name (str):
                The name of the app. This will translate into the name of the
                settings file/directory to make things easy to find.
            default_settings_path (str):
                The path where the settings file should exist.
        """
        super(MacSettings, self).__init__()
        if "win32" == sys.platform:  # pragma: no cover
            # Use the standard Windows config file storage area
            self.settings_file_directory = os.getenv("LOCALAPPDATA")
        elif "darwin" == sys.platform:  # pragma: no cover
            self.settings_file_directory = os.path.expanduser(
                "~/Library/Application Support"
            )
        else:
            # Not using Windows, nor mac so assume Linux/BSD
            self.settings_file_directory = os.path.expanduser("~/.config")

        self.settings_file_directory = (
            f"{self.settings_file_directory}/" f"{app_name}"
        )
        self.settings_file_path = (
            f"{self.settings_file_directory}" f"/{app_name}.yaml"
        )
        self.default_settings_path = default_settings_path
        self.mac_logger = logging.getLogger(mac_logger.LOGGER_NAME)
        self.__app_settings = dict()
        self.__thread_lock = Lock()
        self.events_publisher = MacEventPublisher(self.events)
        if not file_m.does_exist(os_path=self.default_settings_path):
            raise MacSettingsException(
                str_message="The default settings file"
                f" {self.default_settings_path} does "
                "not exist. This is a terminal "
                "failure."
            )
        if not file_m.does_exist(os_path=self.settings_file_path):
            self.mac_logger.info(
                f"The settings file {self.settings_file_path} does "
                "not exist. Creating a new one..."
            )
            self._copy_default_settings()
        # Set the file watchdog to pick up any changes made to the settings
        # file from outside this process.
        self.__file_change_handler = MacSettingsWatchdogHandler()
        self.__settings_file_observer = Observer()
        self.__settings_file_observer.schedule(
            event_handler=self.__file_change_handler,
            path=self.settings_file_path,
            recursive=False,
        )
        self.__settings_file_observer.start()
        # Register ourseleves with the event service to pick up
        # file change notifications.
        self.__file_change_handler.events_publisher.register(
            event_action=self.__file_change_handler.events[0],
            subscriber_callabck=self.reload_settings_from_file,
        )

    def load_settings(self) -> Optional[dict]:
        """
        Load the settings direct from the file.

        Args:
            None

        Return:
            dict:
                A dictionary of the settings in the YAML file to make walking
                the setting very easy.
        """
        # Read the settings from a YAML file.
        try:
            with self.__thread_lock:
                with open(file=self.settings_file_path, mode="rb") as yml_file:
                    self.__app_settings = yaml.safe_load(stream=yml_file)
            self.mac_logger.info("Successfully loaded the settings.")
            print(self.__app_settings)
            change_event = MacEvent(event_action=self.events[1])
            self.events_publisher.post_event(event=change_event)
        except yaml.YAMLError as yaml_error:
            raise MacSettingsException(
                "There was a problem parsing"
                f" the file {self.settings_file_path}"
                f" {yaml_error}"
            )
        return self.__app_settings

    def reload_settings_from_file(self) -> None:
        """
        Reload the settings.

        Args:
            None

        Return:
            None
        """
        self.mac_logger.debug("Reloading the settings from the file.")
        previous_settings = copy.deepcopy(self.__app_settings)
        self.load_settings()
        if previous_settings != self.__app_settings:
            changes = dict_diff(
                dict_a=previous_settings, dict_b=self.__app_settings
            )
            update_event = MacEvent(
                event_action=self.events[0], event_info=changes
            )
            self.events_publisher.post_event(update_event)

    def register_for_events(self, event: str, call_back) -> None:
        """
        Register a callback for a given event.

        Args:
            event (str):
                The name of the event
            call_back (Any):
                The function to execute on callback

        Return:
            None
        """
        self.events_publisher.register(
            event_action=event, subscriber_callabck=call_back
        )
        self.mac_logger.debug(
            f"Registered a callback {call_back} for {event}."
        )

    def unregister_for_events(self, event: str, call_back) -> None:
        """
        Unregister a callback for a given event.

        Args:
            event (str):
                The name of the event
            call_back (Any):
                The function to execute on callback

        Return:
            None
        """
        self.events_publisher.unregister(
            event_action=event, subscriber_callabck=call_back
        )
        self.mac_logger.debug(
            f"Unregistered a callback {call_back} for {event}."
        )

    def __getitem__(self, keys: Any) -> Any:
        """
        Get the value from the underlying settings dictionary.

        Args:
            key (any):
                If querying a muli-level dictionary, this will be a tuple.

        Returns:
            any:
                This could either be the menu, or a subset of the full
                dictionary.
        """
        value = None
        if isinstance(keys, str):
            if keys not in self.__app_settings:
                raise MacSettingsException(
                    f"key {keys} is not in the " "dictionary."
                )
            with self.__thread_lock:
                value = self.__app_settings[keys]
        if isinstance(keys, tuple):
            with self.__thread_lock:
                value = reduce(operator.getitem, keys, self.__app_settings)
        return value

    def __setitem__(self, keys: Any, value: Any) -> None:
        """
        Set the value of an item in the dictionary. This is slightly different
        from the multi-index pattern in that the key names are passed as a
        tuple. For example msettings['level1', 'level2'] = value

        Args:
            keys (any):
                The keys can be either a string, or a tuple
            value (any):
                The value to set the key/value to
        
        Return:
            None
        """
        if isinstance(keys, str):
            with self.__thread_lock:
                self.__app_settings[keys] = value
        else:
            with self.__thread_lock:
                (reduce(operator.getitem, keys[:-1], self.__app_settings))[
                    keys[-1]
                ] = value
        self.__file_change_handler._pause_observer = True
        self.save_settings()
        self.__file_change_handler._pause_observer = False
        changed_setting = {"setting_changed": keys, "new_value": value}
        change_event = MacEvent(
            event_action=self.events[0], event_info=changed_setting
        )
        self.events_publisher.post_event(event=change_event)

    def __contains__(self, keys: Any) -> bool:
        """
        Check whether the key exists

        Args:
            keys (any):
                The name of the key to find. Can be string or tuple.

        Returns:
            bool:
                True or False based on whether the key exists.
        """
        if isinstance(keys, str):
            with self.__thread_lock:
                bool_value = keys in self.__app_settings
        elif isinstance(keys, tuple):
            if keys[0] not in self.__app_settings:
                bool_value = False
            else:
                bool_value = keys[-1] in self.__getitem__(keys[:-1])
        else:
            raise MacSettingsException(
                "Use either a single string or a tuple to query whether"
                " the setting exists."
            )
        return bool_value

    def get_all_settings(self) -> dict:
        """
        Return all settings as a dictionary

        Args:
            None

        Returns:
            dict:
                The settings dictionary
        """
        return self.__app_settings

    def save_settings(self) -> None:
        """
        Save all the settings back to the settings file.

        Args:
            None

        Return:
            None
        """
        try:
            self.mac_logger.debug(
                f"Saving settings to {self.settings_file_path}"
            )
            with self.__thread_lock:
                with open(
                    file=self.settings_file_path,
                    mode="w",
                ) as yml_file:
                    yaml.dump(
                        data=self.__app_settings,
                        stream=yml_file,
                        indent=4,
                        default_flow_style=False,
                        allow_unicode=True,
                        encoding="utf8",
                    )
            self.mac_logger.debug("Successfully saved settings.")
        except Exception as err:
            raise MacSettingsException(f"Unable to save settings. {err}")

    def _copy_default_settings(self) -> None:
        """
        Copy the default settings file into the correct position. If this
        fails we want the exception to break the program flow, so don't try
        and catch any exceptions.

        Args:
            None

        Return:
            None
        """
        parent_directory = pathlib.Path(
            self.settings_file_path
        ).parent.absolute()
        print(self.settings_file_path)
        if not file_m.does_exist(str(parent_directory)):
            self.mac_logger.info(
                "Settings file parent directory needs to be created"
            )
            file_m.create_dir(str(parent_directory))
        self.mac_logger.info("Copying default settings...")
        shutil.copyfile(
            src=self.default_settings_path, dst=self.settings_file_path
        )
        self.mac_logger.info("Default settings copied into place.")


if __name__ == "__main__":  # pragma: no cover
    pass
