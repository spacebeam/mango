# -*- coding: utf-8 -*-
'''
    Mango tasks system logic.
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
from mango.messages import tasks
from mango.messages import BaseResult
from mango.structures.tasks import TaskMap
from riak.datatypes import Map
from mango.tools import clean_structure, clean_results
from tornado import httpclient as _http_client


_http_client.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
http_client = _http_client.AsyncHTTPClient()


class TasksResult(BaseResult):
    '''
        List result
    '''
    results = compound.ListType(compound.ModelType(tasks.Task))


class Tasks(object):
    '''
        Tasks
    '''
    @gen.coroutine
    def get_task(self, account, task_uuid):
        '''
            Get task
        '''
        search_index = 'mango_task_index'
        query = 'uuid_register:{0}'.format(task_uuid)
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # note where the hack change ' to %27 for the url string!
        fq_watchers = "watchers_register:*'{0}'*".format(account.decode('utf8')).replace("'",'%27')
        urls = set()
        urls.add(get_search_item(self.solr, search_index, query, filter_query))
        urls.add(get_search_item(self.solr, search_index, query, fq_watchers))
        # init got response list
        got_response = []
        # init crash message
        message = {'message': 'not found'}
        # ignore riak fields
        IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
        # hopefully asynchronous handle function request
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
            # and know for something completly different!
            for url in urls:
                http_client.fetch(
                    url,
                    callback=handle_request
                )
            while len(got_response) <= 1:
                # Yo, don't be careless with the time!
                yield gen.sleep(0.0010)
            # get stuff from response
            stuff = got_response[0]
            # get it from watchers list
            watchers = got_response[1]
            if stuff['response']['numFound']:
                response = stuff['response']['docs'][0]
                message = clean_response(response, IGNORE_ME)
            elif watchers['response']['numFound']:
                response = watchers['response']['docs'][0]
                message = clean_response(response, IGNORE_ME)
            else:
                logging.error('there is probably something wrong!')
        except Exception as error:
            logging.warning(error)
        return message

    @gen.coroutine
    def get_task_list(self, account, start, end, lapse, status, page_num):
        '''
            Get task list
        '''
        search_index = 'mango_task_index'
        query = 'uuid_register:*'
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # note where the hack change ' to %27 for the url string!
        fq_watchers = "watchers_register:*'{0}'*".format(account.decode('utf8')).replace("'",'%27')
        # page number
        page_num = int(page_num)
        page_size = self.settings['page_size']
        start_num = page_size * (page_num - 1)
        # set of urls
        urls = set()
        urls.add(get_search_list(self.solr, search_index, query, filter_query, start_num, page_size))
        urls.add(get_search_list(self.solr, search_index, query, fq_watchers, start_num, page_size))
        # init got response list
        got_response = []
        # init crash message
        message = {
            'count': 0,
            'page': page_num,
            'results': []
        }
        # ignore riak fields
        IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
        # hopefully asynchronous handle function request
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
            # and know for something completly different!
            for url in urls:
                http_client.fetch(
                    url,
                    callback=handle_request
                )
            while len(got_response) <= 1:
                # Yo, don't be careless with the time!
                yield gen.sleep(0.0010)
            # get stuff from response
            stuff = got_response[0]
            # get it from watchers list
            watchers = got_response[1]
            if stuff['response']['numFound']:
                message['count'] += stuff['response']['numFound']
                for doc in stuff['response']['docs']:
                    message['results'].append(clean_response(doc, IGNORE_ME))
            if watchers['response']['numFound']:
                message['count'] += watchers['response']['numFound']
                for doc in watchers['response']['docs']:
                    message['results'].append(clean_response(doc, IGNORE_ME))
            else:
                logging.error('there is probably something wrong!')
        except Exception as error:
            logging.warning(error)
        return message

    @gen.coroutine
    def new_task(self, struct):
        '''
            New task event
        '''
        search_index = 'mango_task_index'
        bucket_type = 'mango_task'
        bucket_name = 'tasks'
        try:
            event = tasks.Task(struct)
            event.validate()
            event = clean_structure(event)
        except Exception as error:
            raise error
        try:
            structure = {
                "uuid": str(event.get('uuid', str(uuid.uuid4()))),
                "account": str(event.get('account', 'pebkac')),
                "name": str(event.get('title', '')),
                "description": str(event.get('description', '')),
                "payload": str(event.get('payload', '')),
                "assign": str(event.get('assign', '')),
                "public": str(event.get('public', '')),
                "source ": str(event.get('source', '')),
                "destination": str(event.get('destination', '')),
                "labels": str(event.get('labels', '')),
                "start": str(event.get('start', '')),
                "acknowledge": str(event.get('acknowledge', '')),
                "stop": str(event.get('stop', '')),
                "deadline": str(event.get('deadline', '')),
                "duration": str(event.get('duration', '')),
                "comments": str(event.get('comments', '')),
                "history": str(event.get('history', '')),
                "watchers": str(event.get('watchers', '')),
                "status": str(event.get('status', '')),
                "checked": str(event.get('checked', '')),
                "checked_by": str(event.get('checked_by', '')),
                "checked_at": str(event.get('checked_at', '')),
                "created_by": str(event.get('created_by', '')),
                "created_at": str(event.get('created_at', '')),
                "last_update_by": str(event.get('last_update_by', '')),
                "last_update_at": str(event.get('last_update_at', '')),
            }
            result = TaskMap(
                self.kvalue,
                bucket_name,
                bucket_type,
                search_index,
                structure
            )
            message = structure.get('uuid')
        except Exception as error:
            logging.error(error)
            message = str(error)
        return message

    @gen.coroutine
    def modify_task(self, account, task_uuid, struct):
        '''
            Modify task
        '''
        # riak search index
        search_index = 'mango_task_index'
        # riak bucket type
        bucket_type = 'mango_task'
        # riak bucket name
        bucket_name = 'tasks'
        # solr query
        query = 'uuid_register:{0}'.format(task_uuid.rstrip('/'))
        # filter query
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # search query url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        # pretty please, ignore this list of fields from database.
        # if you want to include something in here, remember the _register.
        # example: labels_register.
        IGNORE_ME = ("_yz_id","_yz_rk","_yz_rt","_yz_rb")
        # got callback response?
        got_response = []
        # yours truly
        message = {'update_complete':False}
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
            response = got_response[0].get('response')['docs'][0]
            riak_key = str(response['_yz_rk'])
            bucket = self.kvalue.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
            bucket.set_properties({'search_index': search_index})
            task = Map(bucket, riak_key)
            for key in struct:
                if key not in IGNORE_ME:
                    if type(struct.get(key)) == list:
                        task.reload()
                        old_value = task.registers['{0}'.format(key)].value
                        if old_value:
                            old_list = json.loads(old_value.replace("'",'"'))
                            for thing in struct.get(key):
                                old_list.append(thing)
                            task.registers['{0}'.format(key)].assign(str(old_list))
                        else:
                            new_list = []
                            for thing in struct.get(key):
                                new_list.append(thing)
                            task.registers['{0}'.format(key)].assign(str(new_list))
                    else:
                        task.registers['{0}'.format(key)].assign(str(struct.get(key)))
                    task.update()
            update_complete = True
            message['update_complete'] = True
        except Exception as error:
            logging.exception(error)
        return message.get('update_complete', False)

    @gen.coroutine
    def modify_remove(self, account, task_uuid, struct):
        '''
            Modify remove
        '''
        # riak search index
        search_index = 'mango_task_index'
        # riak bucket type
        bucket_type = 'mango_task'
        # riak bucket name
        bucket_name = 'tasks'
        # solr query
        query = 'uuid_register:{0}'.format(task_uuid.rstrip('/'))
        # filter query
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # search query url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        # pretty please, ignore this list of fields from database.
        # if you want to include something in here, remember the _register.
        # example: labels_register.
        IGNORE_ME = ("_yz_id","_yz_rk","_yz_rt","_yz_rb")
        # got callback response?
        got_response = []
        # yours truly
        message = {'update_complete':False}
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
                # Please, don't be careless with the time.
                yield gen.sleep(0.0010)
            response = got_response[0].get('response')['docs'][0]
            riak_key = str(response['_yz_rk'])
            bucket = self.kvalue.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
            bucket.set_properties({'search_index': search_index})
            task = Map(bucket, riak_key)
            for key in struct:
                if key not in IGNORE_ME:
                    if type(struct.get(key)) == list:
                        task.reload()
                        old_value = task.registers['{0}'.format(key)].value
                        if old_value:
                            old_list = json.loads(old_value.replace("'",'"'))
                            new_list = [x for x in old_list if x not in struct.get(key)]
                            task.registers['{0}'.format(key)].assign(str(new_list))
                            task.update()
                            message['update_complete'] = True
                    else:
                        message['update_complete'] = False
        except Exception as error:
            logging.exception(error)
        return message.get('update_complete', False)

    @gen.coroutine
    def remove_task(self, account, task_uuid):
        '''
            Remove task
        '''
        # Yo, missing history ?
        struct = {}
        struct['status'] = 'deleted'
        message = yield self.modify_task(account, task_uuid, struct)
        return message
