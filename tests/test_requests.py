#! /usr/bin/env python -*- coding: utf-8 -*-
"""
    Name:
        test_requests.py
    Desscription:
        Test the requests functions.
    Version:
        1 - Inital release
    Author:
        J.MacGrillen <macgrillen@gmail.com>
    Copyright:
        Copyright (c) John MacGrillen. All rights reserved.
"""

import maclib.mac_requests as requests


class TestRequests():
    """
    Test the mac_requests class
    """

    m_requests: requests.MacRequests = requests.MacRequests()
    test_headers: dict = {
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Authorization": "Basic"
    }

    def test_01_setting_multiple_headers(self):
        """
        Test we can set multiple headers at once.
        """
        test_headers = {
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Authorization": "Basic"
        }

        self.m_requests.set_all_headers(test_headers)
        assert self.m_requests.http_headers == test_headers

    def test_02_setting_single_header(self):
        """
        Test that we add can add an extra header.
        """
        self.m_requests.set_header(header_key="Accept-Language",
                                   header_value="en-GB")

        assert self.m_requests.http_headers['Accept-Language'] == "en-GB"

    def test_03_send_request(self, monkeypatch):
        """
        Mock the request/response
        """
        
