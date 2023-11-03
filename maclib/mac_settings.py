#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_settigs.py
    Desscription:
        Manage applicatuon settings from a YAML file.
        There should be a set of defaults.
    Version:
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
from typing import Optional
from functools import reduce
import operator
import logging
import yaml
import shutil
import pathlib
import os
import sys
from threading import Lock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import maclib.mac_file_management as file_m
import maclib.mac_logger as mac_logger
from maclib.mac_single import MacSingleInstance
from maclib.mac_exception import MacException


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
    __settings_object: object

    def __init__(self, settings_object: object) -> None:
        """
        Store the main settings object

        Args:
            settings_object (object): Pass in the main settings
            object.
        """
        super(MacSettingsWatchdogHandler).__init__()
        self.mac_logger = logging.getLogger(mac_logger.LOGGER_NAME)
        self.__settings_object = settings_object

    def on_modified(self, event) -> None:
        """
        We're only interested in whether the file has been changed or not.

        Args:
            event (_type_): _description_
        """
        self.mac_logger.debug("File change detected.")
        self.__settings_object.load_settings()
        self.__settings_object.__execute_callbacks()


class MacSettings(metaclass=MacSingleInstance):
    """
    Handle global apps setting using a singleton class.
    Make sure the logger is initialised before calling this class.
    """
    mac_logger: logging.Logger
    settings_file_directory: str
    settings_file_path: str
    default_settings_path: str
    __settings_file_observer: Observer
    __file_change_handler: MacSettingsWatchdogHandler
    __app_settings: dict
    __thread_lock: Lock
    __call_backs: list

    def __init__(self,
                 app_name: str,
                 default_settings_path: str) -> None:
        super(MacSettings, self).__init__()
        if 'win32' == sys.platform:  # pragma: no cover
            # Use the standard Windows config file storage area
            self.settings_file_directory = os.getenv('LOCALAPPDATA')
        elif 'darwin' == sys.platform:  # pragma: no cover
            self.settings_file_directory = os.path.expanduser(
                '~/Library/Application Support')
        else:
            # Not using Windows, nor mac so assume Linux/BSD
            self.settings_file_directory = os.path.expanduser(
                '~/.config')

        self.settings_file_directory = f'{self.settings_file_directory}/' \
                                       f'{app_name}'
        self.settings_file_path = f'{self.settings_file_directory}' \
                                  f'/{app_name}.yaml'
        self.default_settings_path = default_settings_path
        self.mac_logger = logging.getLogger(mac_logger.LOGGER_NAME)
        self.__app_settings = dict()
        self.__thread_lock = Lock()
        self.__call_backs = []
        if not file_m.does_exist(os_path=default_settings_path):
            raise MacSettingsException(
                "The default settings file "
                f"{self.default_settings_path} does not "
                "exist. This is a terminal failure.")
        if not file_m.does_exist(os_path=self.settings_file_path):
            self.mac_logger.info(
                f"The settings file {self.settings_file_path} does "
                "not exist. Creating a new one...")
            self._copy_default_settings()
        self.__file_change_handler = MacSettingsWatchdogHandler(
            settings_object=self)
        self.__settings_file_observer = Observer()
        self.__settings_file_observer.schedule(
            event_handler=self.__file_change_handler,
            path=self.settings_file_path,
            recursive=False)
        self.__settings_file_observer.start()

    def load_settings(self) -> Optional[dict]:
        """
        Load the settings.
        """
        # Read the settings from a YAML file.
        try:
            with self.__thread_lock:
                with open(file=self.settings_file_path,
                          mode='rb') as yml_file:
                    self.__app_settings = yaml.safe_load(stream=yml_file)
            self.mac_logger.info("Successfully loaded the settings.")
        except yaml.YAMLError as yaml_error:
            raise MacSettingsException(
                "There was a problem parsing"
                f" the file {self.settings_file_path}"
                f" {yaml_error}")
        return self.__app_settings

    def __getitem__(self, keys: any) -> any:
        """
        Get the value from the underlying settings dictionary.

        Args:
            key (any): If querying a muli-level dictionary, this will
                       be a tuple.

        Returns:
            any: This could either be the menu, or a subset of the full
                 dictionary.
        """
        value = None
        if isinstance(keys, str):
            if keys not in self.__app_settings:
                raise MacSettingsException(f"key {keys} is not in the "
                                           "dictionary.")
            with self.__thread_lock:
                value = self.__app_settings[keys]
        if isinstance(keys, tuple):
            with self.__thread_lock:
                value = (reduce(operator.getitem, keys, self.__app_settings))
        return value

    def __setitem__(self, keys: any, value: any) -> None:
        """
        Set the value of an item in the dictionary. This is slightly different
        from the multi-index pattern in that the key names are passed as a
        tuple. For example msettings['level1', 'level2'] = value

        Args:
            keys (any): The keys can be either a string, or a tuple
            value (any): The value to set the key/value to.
        """

        if isinstance(keys, str):
            with self.__thread_lock:
                self.__app_settings[keys] = value
        else:
            with self.__thread_lock:
                (reduce(operator.getitem, keys[:-1],
                        self.__app_settings))[keys[-1]] = value
        self.__settings_file_observer.stop()
        self.save_settings()
        self.__settings_file_observer.start()
        self.__execute_callbacks()

    def __contains__(self, keys: any) -> bool:
        """
        Check whether the key exists

        Args:
            keys (any): The name of the key to find. Can be
                        string or tuple.

        Returns:
            bool: True or False based on whether the key exists.
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
                " the setting exists.")
        return bool_value

    def get_all_settings(self) -> dict:
        """
        Return all settings as a dictionary

        Returns:
            dict: The settings dictionary
        """
        return self.__app_settings

    def save_settings(self) -> None:
        """
        Save all the settings back to the settings file.
        """
        try:
            self.mac_logger.debug(
                f"Saving settings to {self.settings_file_path}")
            with self.__thread_lock:
                with open(file=self.settings_file_path,
                          mode='w',) as yml_file:
                    yaml.dump(data=self.__app_settings,
                              stream=yml_file, indent=4,
                              default_flow_style=False,
                              allow_unicode=True,
                              encoding='utf8')
            self.mac_logger.debug("Successfully saved settings.")
        except Exception as err:
            raise MacSettingsException(f"Unable to save settings. {err}")

    def _copy_default_settings(self) -> None:
        """
        Copy the default settings file into the correct position. If this
        fails we want the exception to break the program flow, so don't try
        and catch any exceptions.
        """
        parent_directory = pathlib.Path(
            self.settings_file_path).parent.absolute()
        print(self.settings_file_path)
        if not file_m.does_exist(parent_directory):
            self.mac_logger.info(
                "Settings file parent directory needs to be created")
            file_m.create_dir(parent_directory)
        self.mac_logger.info("Copying default settings...")
        shutil.copyfile(src=self.default_settings_path,
                        dst=self.settings_file_path)
        self.mac_logger.info("Default settings copied into place.")

    def callback_on_change_event(self, call_back_function: object) -> None:
        """
        Register a callback thatwill be called when there's a change
        to the settings file.

        Args:
            call_back_function (object): The function to be called.
        """
        if call_back_function not in self.__call_backs:
            self.__call_backs.append(call_back_function)

    def __execute_callbacks(self) -> None:
        """
        Run though all the callback functions registered.
        """
        [call_back() for call_back in self.__call_backs]


if __name__ == "__main__":  # pragma: no cover
    pass
