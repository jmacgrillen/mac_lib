#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_settings.py
    Desscription:
        Manage application settings. This uses the singleton
        pattern to make sure the setting persist in all modules.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <john.macgrillen@thecodeexpress.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import logging
import yaml
from typing import Optional
import maclib.mac_file_management as file_m
from maclib.mac_single import MacSingleDictionary
import maclib.mac_logger as mac_logger


class MacSettingsFile(MacSingleDictionary):
    """
    cloudEngine uses YAML files for all configuration.
    This is just a simple way of getting at those settings.
    """

    mac_logger: logging.Logger
    settings_file_directory: str
    settings_file_name: str
    settings_file_full_path: str
    able_to_update: bool
    loaded_from_file: bool

    def __init__(self,
                 yaml_file_directory: str = None,
                 yaml_file: str = None) -> None:
        """
        Load the YAML file aready for use
        """
        super(MacSettingsFile, self).__init__()
        self.mac_logger = logging.getLogger(mac_logger.LOGGER_NAME)
        if yaml_file_directory:
            self.settings_file_directory = yaml_file_directory
            if yaml_file:
                self.settings_file_name = yaml_file
            self.settings_file_full_path = "{0}/{1}".format(
                                        yaml_file_directory,
                                        yaml_file)

    def load_settings(self) -> Optional[dict]:
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
        # Read the settings from a YAML file.
        try:
            with open(file=self.settings_file_full_path,
                      mode='rb') as yml_file:
                self.data_dictionary = yaml.safe_load(stream=yml_file)
            self.mac_logger.info("Successfully loaded the settings.")
        except yaml.YAMLError as yaml_error:
            self.mac_logger.error("There was a problem parsing"
                                  " the file %s.\n%s", self.settings_file_name,
                                  yaml_error)
        self.loaded_from_file = True
        return self.data_dictionary

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
                    yaml.dump(data=self.data_dictionary, indent=4))
                yaml.dump(data=self.data_dictionary,
                          stream=yml_file,)
            self.mac_logger.debug("Successfully saved settings.")
        except Exception as err:
            self.mac_logger.error("Unable to save settings. {0}", err)


if __name__ == "__main__":
    pass
