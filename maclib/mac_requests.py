#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Name:
        mac_requests.py
    Description:
        Boiler plate code around requests.
    Version:
        1 - Initial release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import logging
import requests
import maclib.mac_logger as mac_logger


class MacRequests(object):
    """
    Instead of writing the same boiler plate code time after time
    write the basics once.

    Attributes:
        http_headers (dict):
            The headers to be sent with the request.
        mac_logger (logging.Logger):
            The logger for this class.

    Methods:
        set_all_headers(headers: dict) -> None:
            Set all headers at once.
        set_header(header_key: str, header_value: str) -> None:
            Set a particular header.
        send_request(http_action: str, http_url: str) -> requests.Response:
            Send the request.
    """

    http_headers: dict = {}
    mac_logger: logging.Logger

    def __init__(self):
        """
        Class initialisation
        """
        super(MacRequests, self).__init__()
        self.mac_logger = logging.getLogger(mac_logger.LOGGER_NAME)

    def set_all_headers(self, headers: dict) -> None:
        """
        Headers tend to stay the same, so store them once.

        Args:
            headers (dict):
                The headers to be sent with the request.

        Return:
            None
        """
        self.mac_logger.debug("Overwritting all headers")
        self.http_headers = headers

    def set_header(self, header_key: str, header_value: str) -> None:
        """
        Add or update a particular header value.

        Args:
            header_key (str):
                The header key.
            header_value (str):
                The header value.

        Return:
            None
        """
        self.mac_logger.debug(f"Setting header {header_key} to {header_value}")
        self.http_headers[header_key] = header_value

    def send_request(self,
                     http_action: str,
                     http_url: str,
                     ) -> requests.Response:
        """
        Send the request.

        Args:
            http_action (str):
                The http action to take.
            http_url (str):
                The url to send the request to.

        Return:
            requests.Response:
                The response object.
        """
        response: requests.Response = requests.Response()

        self.mac_logger.debug(f"Sending {http_action} request to {http_url}")
        try:
            response = requests.request(
                            method=http_action,
                            url=http_url,
                            headers=self.http_headers
                        )
        except requests.exceptions.RequestException as e:
            self.mac_logger.error(f"Request error {e}")

        return response


if __name__ == "__main__":  # pragma: no cover
    pass
