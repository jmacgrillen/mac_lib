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
import logging
import yaml
import shutil
import pathlib
import collections
from threading import Lock
import mac_file_management as file_m
import mac_logger as mac_logger
from mac_single import MacSingleInstance
from mac_exception import MacException


class MacSettingsException(MacException):
    """
    Exception from MacSettings.
    """
    pass


class MacSettings(object, metaclass=MacSingleInstance):
    """
    Handle global apps setting using a singleton class.
    Make sure the logger is initialised before calling this class.
    """
    mac_logger: logging.Logger
    settings_file_path: str
    default_settings_path: str
    __app_settings: dict
    thread_lock: Lock

    def __init__(self,
                 settings_file_path: str,
                 default_settings_path: str) -> None:
        super(MacSettings, self).__init__()
        self.settings_file_path = settings_file_path
        self.default_settings_path = default_settings_path
        self.mac_logger = logging.getLogger(mac_logger.LOGGER_NAME)
        self.__app_settings = dict()
        self.thread_lock = Lock()
        if not file_m.does_exist(os_path=default_settings_path):
            raise MacSettingsException(
                "The default settings file "
                f"{self.default_settings_path} does not "
                "exist. This is a terminal failure.")
        if not file_m.does_exist(os_path=self.settings_file_path):
            self.mac_logger.info(
                f"The settings file {self.settings_file_path} does "
                "not exist. Creating a new one...")
            self.__copy_default_settings()
        self.load_settings()

    def load_settings(self) -> Optional[dict]:
        """
        Load the settings.
        """
        # Read the settings from a YAML file.
        try:
            self.thread_lock.acquire()
            with open(file=self.settings_file_path,
                      mode='rb') as yml_file:
                self.__app_settings = yaml.safe_load(stream=yml_file)
            self.thread_lock.release()
            self.mac_logger.info("Successfully loaded the settings.")
        except yaml.YAMLError as yaml_error:
            self.mac_logger.error("There was a problem parsing"
                                  " the file %s.\n%s", self.settings_file,
                                  yaml_error)
        return self.__app_settings

    def __getitem__(self, key) -> any:
        """
        Make this class behave like a dictionary

        Args:
            item (str): The name of the key to look for

        Returns:
            any: The dictionary value againts the key
        """
        chainmap = collections.ChainMap()
        chainmap.new_child(key)
        
        #if not self.key_exists(key_name=keys):
        #    raise MacSettingsException(f"Setting {keys} does not exist")
        # self.thread_lock.acquire()
        # setting: any = self.app_settings[key]
        # self.thread_lock.release()
        # return setting

    def __setitem__(self, key, key_value: any) -> None:
        """
        Make this class behave like a dictionary. This will update
        the values in the settings dictionary and save the update.

        Args:
            key (str): The name of the key to save the value against
                       in the dictionary
            key_value (any): The value to save against the supplied key
        """
        self.thread_lock.acquire()
        self.app_settings[key] = key_value
        self.thread_lock.release()
        self.save_settings()

    def get_all_settings(self) -> dict:
        """
        Return all settings as a dictionary

        Returns:
            dict: The settings dictionary
        """
        return self.app_settings

    def save_settings(self) -> None:
        """
        Save all the settings back to the settings file.
        """
        try:
            self.mac_logger.debug(
                f"Saving settings to {self.settings_file_path}")
            self.thread_lock.acquire()
            with open(file=self.settings_file_path,
                      mode='w',) as yml_file:
                yaml.dump(data=self.app_settings,
                          stream=yml_file, indent=4,
                          default_flow_style=False)
            self.thread_lock.release()
            self.mac_logger.debug("Successfully saved settings.")
        except Exception as err:
            self.mac_logger.error(f"Unable to save settings. {err}")

    def key_exists(self, key_name: str) -> bool:
        """
        Check whether the key exists.
        """
        try:
            self.thread_lock.acquire()
            reduce(lambda current_dict, key: current_dict[key],
                   key_depth, self.app_settings)
            self.thread_lock.release()
            return True
        except (KeyError, TypeError):
            return False

    def __copy_default_settings(self) -> None:
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
