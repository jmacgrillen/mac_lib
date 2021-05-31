#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        mac_requests.py
    Desscription:
        Boiler plate code around requests.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import logging
import requests


class CERequests(object):
    """
    Instead of writing the same boiler plate code time after time
    write the basics once.
    """

    http_headers: dict = {}
    mac_logger: logging.Logger

    def __init__(self):
        """
        Class initialisation
        """
        super(CERequests, self).__init__()
        self.mac_logger = logging.getLogger("mac_logger")

    def set_all_headers(self, headers: dict) -> None:
        """
        Headers tend to stay the same, so store them once.
        """
        self.mac_logger.debug("Overwritting all headers")
        self.http_headers = headers

    def set_header(self, header_key: str, header_value: str) -> None:
        """
        Add or update a particular header value.
        """
        self.mac_logger.debug("Setting header {0} to {1}".format(
            header_key,
            header_value
        ))
        self.http_headers[header_key] = header_value

    def send_request(self,
                     http_action: str,
                     http_url: str,
                     ) -> requests.Response:
        """
        Send the request.
        """
        response : requests.Response = requests.Response()

        self.mac_logger.debug("Sending {0} request to {1}".format(
            http_action,
            http_url
        ))
        try:
            response = requests.request(
                            method=http_action,
                            url=http_url,
                            headers=self.http_headers
                        )
        except requests.exceptions.RequestException as e:
            self.mac_logger.error("Request error {0}".format(e))

        return response
