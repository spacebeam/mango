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
<<<<<<< HEAD
from tornado.httpclient import HTTPRequest

from messages import accounts

=======
from tornado import httpclient as httpc
import uuid
>>>>>>> 6c8c5a26f0edc40407e61b3cebcf3c70cfaa4e89
import ujson as json


class UsersTestCase(testing.AsyncTestCase):
<<<<<<< HEAD
    client = testing.AsyncHTTPClient()
    url = "https://api.nonsense.ws/users/"
    headers = {'Content-Type': 'application/json'}
    mock = False
    response = None

    def setUp(self):
        '''
            Setting things up
        '''
=======
    headers = {'Content-Type': 'application/json'}
    url = "https://api.nonsense.ws/users/"
    client = testing.AsyncHTTPClient()
    result = []

    def setUp(self):
>>>>>>> 6c8c5a26f0edc40407e61b3cebcf3c70cfaa4e89
        super().setUp()
        tornado.ioloop.IOLoop.current().run_sync(self.post)

    def tearDown(self):
<<<<<<< HEAD
        '''
            Cleaning up
        '''
        super().tearDown()
        request = HTTPRequest(self.url, method='DELETE')
        response = yield self.client.fetch(request)
        print("Response just after sending DELETE {}".format(response))
=======
        super().tearDown()
>>>>>>> 6c8c5a26f0edc40407e61b3cebcf3c70cfaa4e89
        tornado.ioloop.IOLoop.current().stop()

    @gen.coroutine
    def post(self):
<<<<<<< HEAD
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
=======
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
>>>>>>> 6c8c5a26f0edc40407e61b3cebcf3c70cfaa4e89
