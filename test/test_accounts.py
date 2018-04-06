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
from tornado import httpclient as httpc
import uuid
import ujson as json


class UsersTestCase(testing.AsyncTestCase):
    headers = {'Content-Type': 'application/json'}
    url = "https://api.nonsense.ws/users/"
    client = testing.AsyncHTTPClient()
    result = []

    def setUp(self):
        super().setUp()
        tornado.ioloop.IOLoop.current().run_sync(self.post)

    def tearDown(self):
        super().tearDown()
        tornado.ioloop.IOLoop.current().stop()

    @gen.coroutine
    def post(self):
        user = str(uuid.uuid4())
        # TODO: md5/sha2 your stuff
        data = {'created_by':'https://monteverde.io',
                'account':user,
                'email':'{0}@example.com'.format(user),
                'password':'Letitcrash',
                'status':'testing'}
        request = httpc.HTTPRequest(self.url, 
                                    method='POST',
                                    headers=self.headers,
                                    body=json.dumps(data))
        response = yield self.client.fetch(request)
        self.result.append(response.body)

    @gen_test
    def test_options(self):
        request = httpc.HTTPRequest(self.url,
                                    method='OPTIONS',
                                    headers=self.headers)
        response = yield self.client.fetch(request)
        self.assertIn("200", str(response.code))

    @gen_test
    def test_new_account(self):
        self.assertIn("uuid", str(self.result[0]))
