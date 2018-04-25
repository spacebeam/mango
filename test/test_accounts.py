# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'

# Check our research and resources at the https://nonsense.ws laboratory.


from tornado import gen, testing
from tornado.testing import gen_test

import tornado
import tornado.ioloop

from tornado.httpclient import HTTPRequest

from messages import accounts


import ujson as json


class UsersTestCase(testing.AsyncTestCase):

    client = testing.AsyncHTTPClient()
    url = "https://api.nonsense.ws/users/"
    headers = {'Content-Type': 'application/json'}
    mock = False
    response = None

    def setUp(self):
        '''
            Setting things up
        '''
        super().setUp()
        tornado.ioloop.IOLoop.current().run_sync(self.post)

    def tearDown(self):
        '''
            Cleaning up
        '''
        super().tearDown()
        request = HTTPRequest(self.url, method='DELETE')
        response = yield self.client.fetch(request)
        print("Response just after sending DELETE {0}".format(response.code))
        tornado.ioloop.IOLoop.current().stop()

    @gen.coroutine
    def post(self):
        '''
           Create init request
        '''
        while not self.mock:
            try:
                self.mock = accounts.User.get_mock_object().to_primitive()
            except Exception as error:
                pass
        request = HTTPRequest(self.url, method='POST', headers=self.headers, body=json.dumps(self.mock))
        self.response = yield self.client.fetch(request)

    @gen_test
    def test_check_uuid(self):
        '''
            Check uuid
        '''
        self.assertIn(self.mock.get('uuid'), self.response.body)

    @gen_test
    def test_find_one(self):
        '''
            Find one
        '''
        test = '{0}{1}'.format(self.url, self.mock.get('uuid'))

        print(test)
        response = yield self.client.fetch(test)
        print(response)
        print(response.body)
        print(response.status)
        self.assertIn("{0}".format(self.mock.get('uuid')), str(response.body))

    @gen_test
    def test_options(self):
        request = httpc.HTTPRequest(self.url,
                                    method='OPTIONS',
                                    headers=self.headers)
        response = yield self.client.fetch(request)
        self.assertIn("200", str(response.code))
