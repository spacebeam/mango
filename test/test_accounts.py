from tornado import gen, testing
from tornado.testing import gen_test
import tornado
import tornado.ioloop
import tornado.httpclient

import ujson as json


class UsersTestCase(testing.AsyncTestCase):
    client = testing.AsyncHTTPClient()
    result = []
    url = "https://api.nonsense.ws/users/"
    
    def setUp(self):
        print("Setting up")
        super().setUp()
        tornado.ioloop.IOLoop.current().run_sync(self.post)

    def tearDown(self):
        print("Tearing down")
        super().tearDown()
        request = tornado.httpclient.HTTPRequest(self.url, method='DELETE')
        response = yield self.client.fetch(request)
        print("Response just after sending DELETE {}".format(response))
        tornado.ioloop.IOLoop.current().stop()

    @gen.coroutine
    def post(self):
        print("Posting")
        data = {'created_by':'https://monteverde.io',
                'account':'',
                '':''}
        headers = {'Content-Type': 'application/json'}
        request = tornado.httpclient.HTTPRequest(self.url, method='POST', headers=headers, body=json.dumps(data))
        response = yield self.client.fetch(request)
        print("Response just after sending POST {}".format(response))
        result.append(response.body)
        self.assertIn("201", str(response.code))

    @gen_test
    def test_options(self):
        print('Testing OPTIONS method, getting init information.')
        headers = {'Content-Type': 'application/json'}
        request = tornado.httpclient.HTTPRequest(self.url, method='OPTIONS', headers=headers)
        response = yield self.client.fetch(request)
        print("Response just after sending OPTIONS {0}".format(response.code))
        self.assertIn("200", str(response.code))
