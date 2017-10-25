# -*- coding: utf-8 -*-
'''
    Mango HTTP base handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import uuid
import logging
import ujson as json
from tornado import gen
from tornado import web
from mango.system import basic_authentication
from mango.messages import tasks as _tasks
from mango.messages import accounts as models
from mango.tools import clean_structure, validate_uuid4
from mango import errors
from tornado import httpclient as _http_client

_http_client.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
http_client = _http_client.AsyncHTTPClient()


class BaseHandler(web.RequestHandler):
    '''
        gente d'armi e ganti
    '''
    @property
    def kvalue(self):
        '''
            Key-value database
        '''
        return self.settings['kvalue']

    def initialize(self, **kwargs):
        '''
            Initialize the Base Handler
        '''
        super(BaseHandler, self).initialize(**kwargs)
        # System database
        self.db = self.settings.get('db')
        # System cache
        self.cache = self.settings.get('cache')
        # Page settings
        self.page_size = self.settings.get('page_size')
        # solr riak
        self.solr = self.settings.get('solr')

    def set_default_headers(self):
        '''
            mango default headers
        '''
        self.set_header("Access-Control-Allow-Origin", self.settings.get('domain', '*'))
        #self.set_header("Access-Control-Allow-Origin", self.settings['domain'])

    def get_username_cookie(self):
        '''
            Return the username from a secure cookie (require cookie_secret)
        '''
        return self.get_secure_cookie('username')

    @gen.coroutine
    def check_account_type(self, account):
        '''
            check account type
        '''
        search_index = 'mango_account_index'
        query = 'account_register:{0}'.format(account)
        filter_query = 'account_register:{0}'.format(account)
        #parse and build url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        got_response = []
        # response message
        message = {'message': 'not found'}
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                yield gen.sleep(0.0020) # don't be careless with the time.
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        raise gen.Return(message.get('account_type', 'not found'))

    @gen.coroutine
    def get_permissions(self, account):
        '''
            Get permissions
        '''
        search_index = 'mango_account_index'
        query = 'account_register:{0}'.format(account)
        filter_query = 'account_register:{0}'.format(account)
        #parse and build url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        got_response = []
        # response message
        message = {'message': 'not found'}
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                yield gen.sleep(0.0020) # don't be careless with the time.
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )

        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        raise gen.Return(message.get('permissions', []))


    @gen.coroutine
    def get_account_uuid(self, account):
        '''
            Get valid account uuid
        '''
        logging.info(account)

        search_index = 'mango_account_index'
        query = 'account_register:{0}'.format(account)
        filter_query = 'account_register:{0}'.format(account)
        # parse and build url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        got_response = []
        # clean response message
        message = {}
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                yield gen.sleep(0.0020) # don't be careless with the time.
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        raise gen.Return(message.get('uuid', 'not found'))

    @gen.coroutine
    def get_auth_uuid(self, account, password):
        '''
            Get valid account uuid
        '''
        search_index = 'mango_account_index'
        query = 'password_register:{0}'.format(password)
        filter_query = 'account_register:{0}'.format(account)
        #parse and build url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        got_response = []
        # clean response message
        message = {}
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                yield gen.sleep(0.0020) # don't be careless with the time.
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        raise gen.Return(message.get('uuid', 'not found'))

    @gen.coroutine
    def get_account_labels(self, account):
        '''
            Get account labels
        '''
        search_index = 'mango_account_index'
        query = 'account_register:{0}'.format(account)
        filter_query = 'account_register:{0}'.format(account)
        #parse and build url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        got_response = []
        #response message
        message = {}
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                yield gen.sleep(0.0020) # don't be careless with the time.
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )

        def to_utf8(message):
            final = []
            for item in d:
                if type(item) is dict:
                    result = {}
                    for key, value in item.items():
                        result[str(key)] = str(value)
                    final.append(result)
            return final
        print to_utf8(message) 

        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        raise gen.Return(message.get('labels', []))


@basic_authentication
class LoginHandler(BaseHandler):
    '''
        BasicAuth login
    '''
    @gen.coroutine
    def get(self):
        # clean message
        message = {}
        message['uuid'] = yield self.get_auth_uuid(self.username, self.password)
        message['account_type'] = yield self.check_account_type(self.username)
        message['permissions'] = yield self.get_permissions(self.username)
        message['labels'] = yield self.get_account_labels(self.username)
        if validate_uuid4(message.get('uuid')):
            self.set_header('Access-Control-Allow-Origin','*')
            self.set_header('Access-Control-Allow-Methods','GET, OPTIONS')
            self.set_header('Access-Control-Allow-Headers','Content-Type, Authorization')
            self.set_secure_cookie('username', self.username)
            #account_type
            #self.set_secure_cookie('account_type', str(message['account_type']))
            # permissions
            #self.set_secure_cookie('permissions', str(message['permissions']))
            # yo what is this?
            self.username, self.password = (None, None)
            self.set_status(200)
            self.finish(message)
        else:
            self.set_status(403)
            # I don't know why not 401?
            self.set_header('WWW-Authenticate', 'Basic realm=mango')
            self.finish()

    @gen.coroutine
    def options(self):
        self.set_header('Access-Control-Allow-Origin','*')
        self.set_header('Access-Control-Allow-Methods','GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers','Content-Type, Authorization')
        self.set_status(200)
        self.finish()


class LogoutHandler(BaseHandler):
    '''
        BasicAuth logout
    '''

    @gen.coroutine
    def get(self):
        '''
            Clear secure cookie
        '''
        self.clear_cookie('username')
        self.clear_cookie('labels')
        self.set_status(200)
        self.finish()
