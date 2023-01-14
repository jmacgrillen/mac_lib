#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_settigs.py
    Desscription:
        Manage applicatuon settings from a YAML file.
        There should be a set of defaults.
    Version:
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
from threading import Lock
import maclib.mac_file_management as file_m
import maclib.mac_logger as mac_logger
from maclib.mac_single import MacSingleInstance
from maclib.mac_exception import MacException


class MacSettingsException(MacException):
    """
    Exception from MacSettings.
    """
    pass


class MacSettings(metaclass=MacSingleInstance):
    """
    Handle global apps setting using a singleton class.
    Make sure the logger is initialised before calling this class.
    """
    mac_logger: logging.Logger
    settings_file_path: str
    default_settings_path: str
    __app_settings: dict
    __thread_lock: Lock

    def __init__(self,
                 settings_file_path: str,
                 default_settings_path: str) -> None:
        super(MacSettings, self).__init__()
        self.settings_file_path = settings_file_path
        self.default_settings_path = default_settings_path
        self.mac_logger = logging.getLogger(mac_logger.LOGGER_NAME)
        self.__app_settings = dict()
        self.__thread_lock = Lock()
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
                raise MacException(f"key {keys} is not in the dictionary.")
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
        self.save_settings()

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
        else:
            bool_value = keys[-1] in self.__getitem__(keys[:-1])
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
            self.mac_logger.error(f"Unable to save settings. {err}")

    def _copy_default_settings(self) -> None:
        """
        Copy the default settings file into the correct position. If this
        fails we want the exception to break the program flow, so don't try
        and catch any exceptions.
        """
        parent_directory = pathlib.Path(
            self.settings_file_path).parent.absolute()
        if not file_m.does_exist(parent_directory):
            self.mac_logger.debug(
                "Settings file parent directory needs to be created")
            file_m.create_dir(parent_directory)
        self.mac_logger.debug("Copying default settings...")
        shutil.copyfile(src=self.default_settings_path,
                        dst=self.settings_file_path)
        self.mac_logger.debug("Default settings copied into place.")


if __name__ == "__main__":  # pragma: no cover
    pass
