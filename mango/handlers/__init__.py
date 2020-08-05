# This file is part of mango.

# Distributed under the terms of the last AGPL License.


__author__ = 'Jean Chassoul'


import logging
import ujson as json
from tornado import gen
from tornado import web
from tornado import httpclient as _http_client


_curl_client = 'tornado.curl_httpclient.CurlAsyncHTTPClient'
_http_client.AsyncHTTPClient.configure(_curl_client)
http_client = _http_client.AsyncHTTPClient()


# This is mango's base handler all mango's other handlers are childs of this dude
# So... explain carefully, what the actual fuck are acccout-related functions here? KTHXBYE


class BaseHandler(web.RequestHandler):
    '''
        Process d'armi e ganti
    '''

    def initialize(self, **kwargs):
        '''
            Initialize the Base Handler
        '''
        super(BaseHandler, self).initialize(**kwargs)
        # System database
        self.db = self.settings.get('db')
        # Page settings
        self.page_size = self.settings.get('page_size')
        # Application domain
        self.domain = self.settings.get('domain')

    def set_default_headers(self):
        '''
            default headers
        '''
        self.set_header("Access-Control-Allow-Origin",
                        self.settings.get('domain', '*'))

    @gen.coroutine
    def check_account_type(self, account):
        '''
            check account type
        '''
        search_index = 'mango_account_index'
        query = 'account_register:{0}'.format(account.decode('utf-8'))
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # format and build url
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
                # don't be careless with the time.
                yield gen.sleep(0.0021)
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )
        except Exception as error:
            logging.warning(error)
        return message.get('account_type', 'not found')

    @gen.coroutine
    def get_account_uuid(self, account):
        '''
            Get valid account uuid
        '''
        search_index = 'mango_account_index'
        query = 'account_register:{0}'.format(account.decode('utf-8'))
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # parse and build url
        url = get_search_item(self.solr, search_index, query, filter_query)
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
                # don't be careless with the time.
                yield gen.sleep(0.0021)
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )
        except Exception as error:
            logging.warning(error)
        return message.get('uuid', 'not found')

    @gen.coroutine
    def get_auth_uuid(self, account, password):
        '''
            Get valid account uuid
        '''
        search_index = 'mango_account_index'
        query = 'password_register:{0}'.format(password.decode('utf-8'))
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # parse and build url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        ).replace(' ', '')
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
                # don't be careless with the time.
                yield gen.sleep(0.0021)
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )
        except Exception as error:
            logging.warning(error)
        return message.get('uuid', 'not found')

    @gen.coroutine
    def get_account_labels(self, account):
        '''
            Get account labels
        '''
        search_index = 'mango_account_index'
        query = 'account_register:{0}'.format(account)
        filter_query = 'account_register:{0}'.format(account)
        # parse and build url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        got_response = []
        # response message
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
                # don't be careless with the time.
                yield gen.sleep(0.0021)
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    (key.split('_register')[0], value)
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )
        except Exception as error:
            logging.warning(error)
        return message.get('labels', [])
