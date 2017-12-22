# -*- coding: utf-8 -*-
'''
    Mango accounts system logic.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import uuid
import logging
import ujson as json
from tornado import gen
from schematics.types import compound
from mango.messages import accounts
from mango.messages import BaseResult
from mango.structures.accounts import AccountMap
from riak.datatypes import Map
from mango.tools import clean_structure, clean_results
from tornado import httpclient as _http_client


_http_client.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
http_client = _http_client.AsyncHTTPClient()


class UserResult(BaseResult):
    '''
        List result
    '''
    results = compound.ListType(compound.ModelType(accounts.User))


class Account(object):
    '''
        Account
    '''
    @gen.coroutine
    def get_query_values(self, urls):
        '''
            Process grouped values from Solr
        '''
        process_list = []
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
            else:
                result = json.loads(response.body)
                content = {}
                options = []
                # gunter grass penguin powers
                for stuff in result['grouped']:
                    content['value'] = stuff[0:-9]
                    for g in result['grouped'][stuff]['groups']:
                        options.append(g['groupValue'])
                    content['options'] = options
                # append the final content
                process_list.append(content)
        try:
            for url in urls:
                http_client.fetch(
                    url,
                    callback=handle_request
                )
            while True:
                # this probably make no sense
                # we're just trying to sleep for a nano second in here...
                # or maybe just a millisecond?, I don't know man.
                yield gen.sleep(0.0001)
                if len(process_list) == len(urls):
                    break
                # who fucking cares..
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        finally:
            raise gen.Return(process_list)

    @gen.coroutine
    def get_unique_querys(self, struct):
        '''
            Get unique list from Solr
        '''
        search_index = 'mango_account_index'
        query = 'uuid_register:*'
        filter_query = 'uuid_register:*'
        unique_list = []
        if 'unique' in struct.keys():
            del struct['unique']
        try:
            if len(struct.keys()) == 1:
                for key in struct.keys():
                    field_list = key
                    group_field = key
                    params = {
                        'wt': 'json',
                        'q': query,
                        'fl': field_list,
                        'fq':filter_query,
                        'group':'true',
                        'group.field':group_field,
                    }
                    url = ''.join((
                        self.solr,
                        '/query/',
                        search_index,
                        '?wt=json&q=uuid_register:*&fl=',
                        key,
                        '_register&fq=uuid_register:*&group=true&group.field=',
                        key,
                        '_register'))
                    unique_list.append(url)
            else:
                for key in struct.keys():
                    field_list = key
                    group_field = key
                    params = {
                        'wt': 'json',
                        'q': query,
                        'fl': field_list,
                        'fq':filter_query,
                        'group':'true',
                        'group.field':group_field,
                    }
                    url = ''.join((
                        self.solr,
                        '/query/',
                        search_index,
                        '?wt=json&q=uuid_register:*&fl=',
                        key,
                        '_register&fq=uuid_register:*&group=true&group.field=',
                        key,
                        '_register'))
                    unique_list.append(url)
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        finally:
            raise gen.Return(unique_list)

    @gen.coroutine
    def get_account(self, account, account_uuid):
        '''
            Get account
        '''
        if account is None:
            search_index = 'mango_account_index'
            query = 'uuid_register:{0}'.format(account_uuid)
            #filter_query = 'account_register:{0}'.format(account)
            url = "https://{0}/search/query/{1}?wt=json&q={2}".format(
                self.solr, search_index, query
            )
        elif account is not None:
            search_index = 'mango_account_index'
            query = 'uuid_register:{0}'.format(account_uuid)
            filter_query = 'account_register:{0}'.format(account)
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
    def get_account_list(self, account, start, end, lapse, status, page_num):
        '''
            Get account list
        '''
        if account is None:
            search_index = 'mango_account_index'
            query = 'uuid_register:*'
            page_num = int(page_num)
            page_size = self.settings['page_size']
            start_num = page_size * (page_num - 1)
            active = 'active'
            filter_query = 'status_register:{0}'.format(active)
            url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}&start={4}&rows={5}&sort=created_at_register+desc".format(
                self.solr, search_index, query, filter_query, start_num, page_size
            )
        elif account is not None:
            search_index = 'mango_account_index'
            query = 'uuid_register:*'
            filter_query = 'created_by_register:{0}'.format(account)
            page_num = int(page_num)
            page_size = self.settings['page_size']
            start_num = page_size * (page_num - 1)
            active = 'active'
            filter_query_two = 'status_register:{0}'.format(active)
            url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}&fq={4}&start={5}&rows={6}&sort=created_at_register+desc".format(
                self.solr, search_index, query, filter_query, filter_query_two, start_num, page_size
            )
        von_count = 0
        got_response = []
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
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        finally:
            raise gen.Return(got_response[0])

    @gen.coroutine
    def new_account(self, struct):
        '''
            New account event
        '''
        search_index = 'mango_account_index'
        bucket_type = 'mango_account'
        bucket_name = 'accounts'
        try:
            event = accounts.User(struct)
            event.validate()
            event = clean_structure(event)
        except Exception, e:
            raise e
        try:
            message = event.get('uuid')
            structure = {
                "uuid": str(event.get('uuid', str(uuid.uuid4()))),
                "account": str(event.get('account', 'pebkac')),
                "active": str(event.get('active', '')),
                "status": str(event.get('status', '')),
                "name": str(event.get('name', '')),
                "first_name": str(event.get('first_name', '')),
                "last_name": str(event.get('last_name', '')),
                "middle_name": str(event.get('middle_name', '')),
                "description": str(event.get('description', '')),
                "account_type": str(event.get('account_type', '')),
                "password": str(event.get('password', '')),
                "email": str(event.get('email', '')),
                "is_admin": str(event.get('is_admin', '')),
                "phone_number": str(event.get('phone_number', '')),
                "extension": str(event.get('extension', '')),
                "country_code": str(event.get('country_code', '')),
                "timezone": str(event.get('timezone', '')),
                "company": str(event.get('company', '')),
                "location": str(event.get('location', '')),
                "membership": str(event.get('membership', '')),
                "url": str(event.get('url', '')),
                "max_channels": str(event.get('max_channels', '')),
                "checksum": str(event.get('checksum', '')),
                "checked": str(event.get('checked', '')),
                "created_by": str(event.get('created_by', '')),
                "created_at": str(event.get('created_at', '')),
                "last_update_at": str(event.get('last_update_at', '')),
                "last_update_by": str(event.get('last_update_by', '')),
                "members": str(event.get('members', '')),
                "phones": str(event.get('phones', '')),
                "emails": str(event.get('emails', '')),
                "history": str(event.get('history', '')),
                "layouts": str(event.get('layouts', '')),
                "labels": str(event.get('labels', '')),
                "orgs": str(event.get('orgs', '')),
                "groups": str(event.get('groups', '')),
                "resources": str(event.get('resources', '')),
                "hashs": str(event.get('hashs', '')),
                "permissions": str(event.get('permissions', '')),
                "resource": str(event.get('resource', '')),
                "resource_uuid": str(event.get('resource_uuid', '')),
                "active": str(event.get('active', '')),
            }
            result = AccountMap(
                self.kvalue,
                bucket_name,
                bucket_type,
                search_index,
                structure
            )
        except Exception, e:
            logging.error(e)
            message = str(e)
        raise gen.Return(message)

    @gen.coroutine
    def modify_account(self, account, account_uuid, struct):
        '''
            Modify account
        '''
        # riak search index
        search_index = 'mango_account_index'
        # riak bucket type
        bucket_type = 'mango_account'
        # riak bucket name
        bucket_name = 'accounts'
        # solr query
        query = 'uuid_register:{0}'.format(account_uuid.rstrip('/'))
        # filter query
        filter_query = 'account_register:{0}'.format(account)
        # search query url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        # pretty please, ignore this list of fields from database.
        IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb","checked","keywords"]
        got_response = []
        update_complete = False
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
                yield gen.sleep(0.0010)
            response_doc = got_response[0].get('response')['docs'][0]
            riak_key = str(response_doc['_yz_rk'])
            bucket = self.kvalue.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
            bucket.set_properties({'search_index': search_index})
            contact = Map(bucket, riak_key)
            for key in struct:
                if key not in IGNORE_ME:
                    contact.registers['{0}'.format(key)].assign(str(struct.get(key)))
            contact.update()
            update_complete = True
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        finally:
            raise gen.Return(update_complete)

    @gen.coroutine
    def remove_account(self, account, account_uuid):
        '''
            Remove account
        '''
        struct = {}
        struct['status'] = 'deleted'
        message = yield self.modify_account(account, account_uuid, struct)
        raise gen.Return(message)
