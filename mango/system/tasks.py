# -*- coding: utf-8 -*-
'''
    Mango tasks system logic.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import uuid
import urllib
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
        search_index = 'mango_task_index'
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
                        'https://api.cloudforest.ws/search/query/',
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
                        'https://api.cloudforest.ws/search/query/',
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
    def get_task(self, account, task_uuid):
        '''
            Get task
        '''
        search_index = 'mango_task_index'
        query = 'uuid_register:{0}'.format(task_uuid)
        filter_query = 'account_register:{0}'.format(account)
        # build the url
        url = "https://api.cloudforest.ws/search/query/{0}?wt=json&q={1}&fq={2}".format(
            search_index, query, filter_query
        )
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
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response_doc = stuff['response']['docs'][0]
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message = dict(
                    # key, value
                    (key.split('_register')[0], value) 
                    for (key, value) in response_doc.items()
                    if key not in IGNORE_ME
                )
            else:
                message = {'message': 'not found'}
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)
        finally:
            raise gen.Return(message)

    @gen.coroutine
    def get_task_list(self, account, start, end, lapse, status, page_num):
        '''
            Get task list
        '''
        search_index = 'mango_task_index'
        query = 'uuid_register:*'
        filter_query = 'account_register:{0}'.format(account)
        page_num = int(page_num)
        page_size = self.settings['page_size']
        url = "https://api.cloudforest.ws/search/query/{0}?wt=json&q={1}&fq={2}".format(
            search_index, query, filter_query
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
    def new_task(self, struct):
        '''
            New task event
        '''
        # currently we are changing this in two steps, first create de index with a structure file
        search_index = 'mango_task_index'
        # on the riak database with riak-admin bucket-type create `bucket_type`
        # remember to activate it with riak-admin bucket-type activate
        bucket_type = 'mango_task'
        # the bucket name can be dynamic
        bucket_name = 'tasks'
        try:
            event = tasks.Task(struct)
            event.validate()
            event = clean_structure(event)
        except Exception, e:
            raise e
        try:
            message = event.get('uuid')
            structure = {
                "uuid": str(event.get('uuid', str(uuid.uuid4()))),
                "account": str(event.get('account', 'pebkac')),
                 "title": str(event.get('title', '')),
                "description": str(event.get('description', '')),
                "payload": str(event.get('payload', '')),
                "assignees": str(event.get('assignees', '')),
                "public": str(event.get('public', '')),
                "source ": str(event.get('source', '')),
                "destination": str(event.get('destination', '')),
                "labels": str(event.get('labels', '')),
                "uri": str(event.get('uri', '')),
                "start": str(event.get('start', '')),
                "ack": str(event.get('ack', '')),
                "stop": str(event.get('stop', '')),
                "deadline": str(event.get('deadline', '')),
                "duration": str(event.get('duration', '')),
                "comments": str(event.get('comments', '')),
                "status": str(event.get('status', '')),
                "checked": str(event.get('checked', '')),
                "checked_by": str(event.get('checked_by', '')),
                "last_update_by": str(event.get('last_update_by', '')),
                "last_update_at": str(event.get('last_update_at', '')),
                "created_by": str(event.get('created_by', '')),
                "created_at": str(event.get('created_at', '')),
                "last_modified": str(event.get('last_modified', '')),
                "checksum": str(event.get('checksum', '')),
                "'comments_total": str(event.get('comments_total', '')),
                "hashs": str(event.get('hashs', '')),
                "hashs_total": str(event.get('hashs_total', '')),
                "assignees_total": str(event.get('assignees_total', '')),
                "history": str(event.get('history', '')),
                "history_total": str(event.get('history_total', '')),
                "labels_total": str(event.get('labels_total', '')),
            }
            result = TaskMap(
                self.kvalue,
                bucket_name,
                bucket_type,
                search_index,
                structure
            )
            def handle_request(response):
                '''
                    Request Async Handler
                '''
                if response.error:
                    logging.error(response.error)
                else:
                    logging.warning(response.body)

            # I almost die reading this WTF ?????????????????????????????????????????????????????

            # missing secrets, missing secrets, missing secrets, missing secrets, missing secrets
            
            # missing secrets current info for gigatech lolol

            # missing secrets, missing secrets, missing secrets, missing secrets, missing secrets

            #pis_u = 'mail'
            #ola_r = 'gun'
            #gun_l = '/v{0}/gigatechsupport.com/'.format('3') + 'messages'
            #hammer_in = 'f2309bfe6'
            #hammer_out = '3dfdabc'
            #hammer_wut = 'a81966e2f0458f5f'
            #url = 'https://api.{0}{1}.net{2}'.format(pis_u, ola_r, gun_l)
            #melon = 'key-{0}{1}{2}'.format(hammer_wut, hammer_in, hammer_out)

            pis_u = 'mail'
            ola_r = 'gun'
            gun_l = '/v{0}/fioin.com/'.format('3') + 'messages'
            hammer_in = '96c209f169f8'
            hammer_wut = 'c962530294e'          
            hammer_out = 'ad7755e0c'
            url = 'https://api.{0}{1}.net{2}'.format(pis_u, ola_r, gun_l)
            melon = 'key-{0}{1}{2}'.format(hammer_wut, hammer_in, hammer_out)

            body = urllib.urlencode({
                "to": structure['destination'],
                "from": structure['source'],
                "subject": structure['subject'],
                "text": structure['text'],
                "html": structure['html']
            })
            http_client.fetch(
                url,
                body=body,
                method='POST',
                auth_username='api',
                auth_password=melon,
                callback=handle_request
            )
            # missing secrets, missing secrets, missing secrets, missing secrets, missing secrets

            # missing secrets current info for gigatech lolol
            
            # missing secrets, missing secrets, missing secrets, missing secrets, missing secrets
        except Exception, e:
            logging.error(e)
            message = str(e)
        raise gen.Return(message)

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
        filter_query = 'account_register:{0}'.format(account)
        # search query url
        url = "https://api.cloudforest.ws/search/query/{0}?wt=json&q={1}&fq={2}".format(
            search_index, query, filter_query
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
    def remove_task(self, account, task_uuid):
        '''
            Remove task
        '''
        # missing history
        struct = {}
        struct['status'] = 'deleted'
        test = yield self.modify_task(account, task_uuid, struct)
        logging.info(test)
        raise gen.Return(test)