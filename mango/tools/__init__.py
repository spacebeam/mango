# -*- coding: utf-8 -*-
'''
    Mango tools system logic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import time
import arrow
import ujson as json
import logging
import uuid
import urllib
from tornado import gen
from mango import errors
from mango.messages import accounts
from tornado import httpclient as _http_client

_http_client.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
http_client = _http_client.AsyncHTTPClient()


def validate_uuid4(uuid_string):
    '''
    Validate that a UUID string is in
    fact a valid uuid4.

    Happily, the uuid module does the actual
    checking for us.
    '''
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False
    return str(val) == uuid_string

def get_average(total, marks):
    '''
        Get average from signals
    '''
    return float(total) / len(marks)

def get_percentage(shit, stuff):
    '''
        Get percentage of shit and stuff.

    '''
    return "{:.0%}".format(shit/stuff)

@gen.coroutine
def check_json(struct):
    '''
        Check for malformed JSON
    '''
    try:
        struct = json.loads(struct)
    except Exception, e:
        api_error = errors.Error(e)
        error = api_error.json()
        raise gen.Return(error)
        return
    raise gen.Return(struct)

@gen.coroutine
def check_account_type(self, account, account_type):
    '''
        check account type
    '''
    search_index = 'mango_account_index'
    query = 'account_type_register:{0}'.format(account_type)
    filter_query = 'account_register:{0}'.format(account)
    # url building
    
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
    raise gen.Return(message)

@gen.coroutine
def get_account_uuid(self, account, password):
    '''
        Get valid account uuid
    '''
    search_index = 'mango_account_index'
    query = 'password_register:{0}'.format(password)
    filter_query = 'account_register:{0}'.format(account)
    # yo! url building
    url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
        self.solr, search_index, query, filter_query
    )
    logging.info('get_account_uuid hi: {0}'.format(url))
    # got response?
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
    # url building
    
    url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
        self.solr, search_index, query, filter_query
    )
    logging.info(url)

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
    raise gen.Return(message.get('labels', []))

@gen.coroutine
def check_times(start, end):
    '''
        Check times
    '''
    try:
        start = (arrow.get(start) if start else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))
        # so... 2 lines more just for the fucking timestamp?
        start = start.timestamp
        end = end.timestamp
    except Exception, e:
        logging.exception(e)
        raise e
        return
    message = {'start':start, 'end':end}
    raise gen.Return(message)

@gen.coroutine
def check_times_get_timestamp(start, end):
    '''
        Check times get timestamp
    '''
    try:
        start = (arrow.get(start) if start else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))
    except Exception, e:
        logging.exception(e)
        raise e
        return
    message = {'start':start.timestamp, 'end':end.timestamp}
    raise gen.Return(message)

@gen.coroutine
def check_times_get_datetime(start, end):
    '''
        Check times get datetime
    '''
    try:
        start = (arrow.get(start) if start else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))
    except Exception, e:
        logging.exception(e)
        raise e
        return
    message = {'start':start.naive, 'end':end.naive}
    raise gen.Return(message)

@gen.coroutine
def new_resource(db, struct, collection=None):
    '''
        New resource function
    '''
    import uuid as _uuid
    from schematics import models as _models
    from schematics import types as _types
    # class MangoResource schematics model.
    class MangoResource(_models.Model):
        '''
            Mango resource
        '''
        uuid = _types.UUIDType(default=_uuid.uuid4)
        account = _types.StringType(required=False)
        resource  = _types.StringType(required=True)
    # Calling getattr(x, "foo") is just another way to write x.foo
    collection = getattr(db, collection)
    # the spawning pool of introspection.
    try:
        message = MangoResource(struct)
        message.validate()
        message = message.to_primitive()
    except Exception, e:
        logging.exception(e)
        raise e
        return
    resource = 'resources.{0}'.format(message.get('resource'))
    try:
        message = yield collection.update(
            {
                'account': message.get('account')
            },
            {
                '$addToSet': {
                    '{0}.contains'.format(resource): message.get('uuid')
                },
                '$inc': {
                    'resources.total': 1,
                    '{0}.total'.format(resource): 1
                }
            }
        )
    except Exception, e:
        logging.exception(e)
        raise e
        return
    raise gen.Return(message)

def clean_message(struct):
    '''
        clean message
    '''
    struct = struct.to_native()
    struct = {
        key: struct[key] 
            for key in struct
                if struct[key] is not None
    }
    return struct

def clean_structure(struct):
    '''
        clean structure
    '''
    struct = struct.to_primitive()
    struct = {
        key: struct[key] 
            for key in struct
                if struct[key] is not None
    }
    return struct

def clean_results(results):
    '''
        clean results
    '''
    results = results.to_primitive()
    results = results.get('results')
    results = [
        {
            key: dic[key]
                for key in dic
                    if dic[key] is not None 
        } for dic in results 
    ]
    return {'results': results}

def str2bool(boo):
    '''
        String to boolean
    '''
    return boo.lower() in ('yes', 'true', 't', '1')