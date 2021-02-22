#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        ce_settings.py
    Desscription:
        The Code Express settinsg file manager.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <john.macgrillen@thecodeexpress.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import logging
import yaml
import mac_lib.mac_file_management as file_m


class CESettingsFile(object):
    """
    cloudEngine uses YAML files for all configuration.
    This is just a simple way of getting at those settings.
    """

    mac_logger: logging.Logger = logging.getLogger("mac_logger")
    settings_file_directory: str = None
    settings_file_name: str = None
    settings_file_full_path: str = None
    settings: dict = None
    able_to_update: bool = False
    __instance = None
    loaded_from_file: bool = None

    def __init__(self,
                 yaml_file_directory: str = None,
                 yaml_file: str = None) -> None:
        """
        Load the YAML file aready for use
        """
        if yaml_file_directory:
            self.settings_file_directory = yaml_file_directory
            self.settings_file_name = yaml_file
            self.settings_file_full_path = "{0}/{1}".format(
                                        yaml_file_directory,
                                        yaml_file)

    def __new__(cls, *args, **kwargs):
        """
        This class is following the Singleton pattern, a class that
        is a single instance that persists across all modules no matter
        how many times the program calls for a new instance.
        """
        if not cls.__instance:
            cls.__instance = super(CESettingsFile, cls).__new__(
                                cls, *args, **kwargs)
        return cls.__instance

    def load_settings(self) -> dict:
        """
        Load the settings.
        """
        # Check the file exists before trying to open it
        if not file_m.does_exist(os_path=self.settings_file_full_path):
            self.mac_logger.info(
                "The settings file %s does not exist. Creating a new one...",
                self.settings_file_full_path)
            if not file_m.does_exist(os_path=self.settings_file_directory):
                if not file_m.create_dir(
                            dir_path=self.settings_file_directory):
                    err_msg = "Could not create the settings " \
                              "directory {0}".format(
                                    self.settings_file_directory)
                    self.mac_logger.error(err_msg)
                    return None
                else:
                    self.save_settings()

        # Read the yaml file.
        try:
            with open(file=self.settings_file_full_path,
                      mode='rb') as yml_file:
                self.settings = yaml.safe_load(stream=yml_file)
            self.mac_logger.info("Successfully loaded the settings.")
        except yaml.YAMLError as yaml_error:
            self.mac_logger.error("There was a problem parsing"
                                 " the file %s.\n%s", self.settings_file_name,
                                 yaml_error)
        self.loaded_from_file = True
        return self.settings

    def save_settings(self) -> None:
        """
        Save all the settings back to the settings file.
        """
        try:
            self.mac_logger.debug("Saving settings to {}".format(
                self.settings_file_full_path
            ))
            with open(file=self.settings_file_full_path,
                      mode='w',) as yml_file:
                self.mac_logger.debug(
                    yaml.dump(data=self.settings, indent=4))
                yaml.dump(data=self.settings,
                          stream=yml_file,)
            self.mac_logger.debug("Successfully saved settings.")
        except Exception as err:
            self.mac_logger.error("Unable to save settings. {0}", err)

    def does_key_exist(self, key_name: str) -> bool:
        """
        Check whether the file contains the requested key.
        """
        if key_name not in self.settings:
            return False
        return True

    def __setitem__(self, setting_key: str, settings_value) -> None:
        """
        Update the settings.
        """
        self.mac_logger("Saving setting {0}.".format(setting_key))
        self.settings[setting_key] = settings_value
        self.save_settings()

    def __getitem__(self, key: str) -> str:
        """
        When requested return the value of a particular key.
        """
        if not self.settings:
            self.mac_logger.error(
                "No settings are available.")
            return None
        try:
            setting = self.settings[key]
        except AttributeError as a_error:
            self.mac_logger.error(a_error)
            return None
        return setting


if __name__ == "__main__":
    pass
