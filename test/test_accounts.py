# -*- coding: utf-8 -*-
# This file is part of mango.

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import schematics

from tornado import gen, testing
from tornado.testing import gen_test
from tornado.ioloop import IOLoop
from tornado.httpclient import HTTPRequest

import ujson as json

from schemas import accounts


class UsersTestCase(testing.AsyncTestCase):
    """
    Users Test Case
    """

    client = testing.AsyncHTTPClient()
    url = "http://127.0.0.1/users/"
    headers = {"Content-Type": "application/json"}
    mock = False
    response = None

    def setUp(self):
        """
        Setting things up
        """
        super().setUp()
        warnings.filterwarnings(
            "ignore", category=schematics.deprecated.SchematicsDeprecationWarning
        )
        IOLoop.current().run_sync(self.post)

    def tearDown(self):
        """
        Cleaning up
        """
        super().tearDown()
        request = HTTPRequest(self.url, method="DELETE")
        response = yield self.client.fetch(request)
        print("Response just after sending DELETE {0}".format(response.code))
        IOLoop.current().stop()

    @gen.coroutine
    def post(self):
        """
        Create init request
        """
        while not self.mock:
            try:
                self.mock = accounts.Users.get_mock_object().to_primitive()
            except Exception as error:
                pass
        request = HTTPRequest(
            self.url, method="POST", headers=self.headers, body=json.dumps(self.mock)
        )
        self.response = yield self.client.fetch(request)

    @gen_test
    def test_check_uuid(self):
        """
        Check uuid
        """
        self.assertIn(self.mock.get("uuid"), str(self.response.body))

    @gen_test
    def test_options(self):
        """
        OPTIONS
        """
        request = HTTPRequest(self.url, method="OPTIONS")
        response = yield self.client.fetch(request)
        self.assertEqual(response.code, 200)

    @gen_test
    def test_find_one(self):
        """
        Find one
        """
        url = "{0}{1}".format(self.url, str(self.mock.get("uuid")))
        request = HTTPRequest(url, method="GET", headers=self.headers)
        response = yield self.client.fetch(request)
        self.assertIn(self.mock.get("uuid"), str(response.body))

    @gen_test
    def test_find_all(self):
        """
        Find all
        """
        request = HTTPRequest(self.url, method="GET", headers=self.headers)
        response = yield self.client.fetch(request)
        self.assertEqual(response.code, 200)
