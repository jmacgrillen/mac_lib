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
import maclib.mac_requests as mac_requests
import json
import responses
import requests


class TestRequests():
    """
    Test the mac_requests class
    """

    m_requests: mac_requests.MacRequests = mac_requests.MacRequests()
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

    @responses.activate
    def test_03_send_request(self):
        """
        Mock the request/response
        """
        return_code = 200
        test_url = "https://www.madethisup.test/"

        test_body = {
            'id': 'test1',
            'name': 'Test1',
            'description': 'This is a Test',
            'imageUrl': './my_image.jpg'
        }

        responses.add(
            responses.Response(
                method='GET',
                url=test_url,
                body=json.dumps(test_body),
                headers=self.m_requests.http_headers,
                content_type='application/json',
                status=return_code)
        )

        response = self.m_requests.send_request('GET',
                                                test_url)

        assert len(responses.calls) == 1
        assert responses.calls[0].request.url == test_url
        assert response.status_code == return_code
        assert response.text == json.dumps(test_body)

    def test_04_send_exception(self, monkeypatch):
        """
        Test that the exception is caught
        """
        test_url = "https://www.madethisup.test/"
        http_method = 'GET'

        def raise_exception(method: str,
                            url: str,
                            headers):
            """
            Make sure the request raises an exception
            """
            assert method == http_method
            assert url == test_url
            assert headers == self.m_requests.http_headers
            raise requests.exceptions.RequestException("Test message")

        monkeypatch.setattr(requests, 'request', raise_exception)
        response = self.m_requests.send_request(http_method, test_url)
        assert response.request is None
