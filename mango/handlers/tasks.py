# -*- coding: utf-8 -*-
'''
    HTTP tasks handlers.
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
from mango.messages import tasks as models
from mango.system import tasks
from tornado import httpclient
from mango.tools import errors, str2bool, check_json, new_resource # <!--------------------   NEW RESOURCE 
from mango.handlers import BaseHandler


class Handler(tasks.Tasks, BaseHandler):
    '''
        HTTP request handlers
    '''

    @gen.coroutine
    def head(self, account=None, task_uuid=None, page_num=0):
        '''
            Head tasks
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_current_username()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # not unique
        unique = query_args.get('unique', False)
        # rage against the finite state machine
        status = 'all'
        # are we done yet?
        done = False
        # some random that crash this shit
        message = {'crashing': True}
        # unique flag activated
        if unique:
            unique_stuff = {key:query_args[key][0] for key in query_args}
            query_list = yield self.get_unique_querys(unique_stuff)
            unique_list = yield self.get_query_values(query_list)
            done = True
            message = {'tasks':unique_list}
            self.set_status(200)
        # get task list
        if not done and not task_uuid:
            task_list = yield self.get_task_list(account, start, end, lapse, status, page_num)
            message = {
                'count': task_list.get('response')['numFound'],
                'page': page_num,
                'results': []
            }
            for doc in task_list.get('response')['docs']:
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message['results'].append(
                    dict((key.split('_register')[0], value) 
                    for (key, value) in doc.items() if key not in IGNORE_ME)
                )
            self.set_status(200)
        # single task received
        if not done and task_uuid:
            # try to get stuff from cache first
            task_uuid = task_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('tasks:{0}'.format(task_uuid))
            if message is not None:
                logging.info('tasks:{0} done retrieving from cache!'.format(task_uuid))
                self.set_status(200)
            else:
                message = yield self.get_task(account, task_uuid)
                if self.cache.add('tasks:{0}'.format(task_uuid), data, 1):
                    logging.info('new cache entry {0}'.format(str(task_uuid)))
                    self.set_status(200)
            if not message:
                self.set_status(400)
                message = {'missing account {0} task_uuid {1} page_num {2} checked {3}'.format(
                    account, task_uuid, page_num, checked):message}
        # thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def get(self, account=None, task_uuid=None, start=None, end=None, page_num=1, lapse='hours'):
        '''
            Get tasks
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_current_username()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # not unique
        unique = query_args.get('unique', False)
        # rage against the finite state machine
        status = 'all'
        # are we done yet?
        done = False
        # some random that crash this shit
        message = {'crashing': True}
        # unique flag activated
        if unique:
            unique_stuff = {key:query_args[key][0] for key in query_args}
            query_list = yield self.get_unique_querys(unique_stuff)
            unique_list = yield self.get_query_values(query_list)
            done = True
            message = {'tasks':unique_list}
            self.set_status(200)
        # get task list
        if not done and not task_uuid:
            task_list = yield self.get_task_list(account, start, end, lapse, status, page_num)
            message = {
                'count': task_list.get('response')['numFound'],
                'page': page_num,
                'results': []
            }
            for doc in task_list.get('response')['docs']:
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message['results'].append(
                    dict((key.split('_register')[0], value) 
                    for (key, value) in doc.items() if key not in IGNORE_ME)
                )
            self.set_status(200)
        # single task received
        if not done and task_uuid:
            # try to get stuff from cache first
            task_uuid = task_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('tasks:{0}'.format(task_uuid))
            if message is not None:
                logging.info('tasks:{0} done retrieving from cache!'.format(task_uuid))
                self.set_status(200)
            else:
                data = yield self.get_task(account, task_uuid)
                if self.cache.add('tasks:{0}'.format(task_uuid), data, 1):
                    logging.info('new cache entry {0}'.format(str(task_uuid)))
                    self.set_status(200)
            if not message:
                self.set_status(400)
                message = {'missing account {0} task_uuid {1} page_num {2} checked {3}'.format(
                    account, task_uuid, page_num, checked):message}
        # thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def post(self):
        '''
            Create task
        '''
        struct = yield check_json(self.request.body)
        format_pass = (True if struct and not struct.get('errors') else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        # request query arguments
        query_args = self.request.arguments
        # get account from new task struct
        account = struct.get('account', None)
        # get the current frontend logged username
        username = self.get_current_username()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # execute new task struct
        ack = yield self.new_task(struct)
        # complete message with receive acknowledgment uuid.
        message = {'uuid':ack}
        if 'error' in message['uuid']:
            scheme = 'task'
            reason = {'duplicates': [
                (scheme, 'account'),
                (scheme, 'uuid')
            ]}
            message = yield self.let_it_crash(struct, scheme, message['uuid'], reason)
            self.set_status(400)
        else:

            # start work on rew resources implementation on riak kv

            link_reference = yield new_resource('tasks', message, struct)

            # please test this shit out

            self.set_status(201)
        self.finish(message)

    @gen.coroutine
    def patch(self, task_uuid):
        '''
            Modify task
        '''
        struct = yield check_json(self.request.body)
        format_pass = (True if not dict(struct).get('errors', False) else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        account = self.request.arguments.get('account', [None])[0]
        if not account:
            # if not account we try to get the account from struct
            account = struct.get('account', None)
        result = yield self.modify_task(account, task_uuid, struct)
        if not result:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('task', task_uuid)
            self.finish(error)
            return
        self.set_status(200)
        self.finish({'message': 'update completed successfully'})

    @gen.coroutine
    def delete(self, task_uuid):
        '''
            Delete task
        '''
        query_args = self.request.arguments
        account = query_args.get('account', [None])[0]
        result = yield self.remove_task(account, task_uuid)
        if not result:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('task', task_uuid)
            self.finish(error)
            return
        self.set_status(204)
        self.finish()

    @gen.coroutine
    def options(self, task_uuid=None):
        '''
            Resource options
        '''
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PATCH, DELETE, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', ''.join(('Accept-Language,',
                        'DNT,Keep-Alive,User-Agent,X-Requested-With,',
                        'If-Modified-Since,Cache-Control,Content-Type,',
                        'Content-Range,Range,Date,Etag')))
        # allowed http methods
        message = {
            'Allow': ['HEAD', 'GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS']
        }
        # resource parameters
        parameters = {}
        # mock your stuff
        stuff = models.Task.get_mock_object().to_primitive()
        for k, v in stuff.items():
            if v is None:
                parameters[k] = str(type('none'))
            elif isinstance(v, unicode):
                parameters[k] = str(type('unicode'))
            else:
                parameters[k] = str(type(v))
        # after automatic madness return description and parameters
        # we now have the option to clean a little bit.
        parameters['labels'] = 'array/string'
        # end of manual cleaning
        POST = {
            "description": "Create task",
            "parameters": parameters
        }
        # filter single resource
        if not task_uuid:
            message['POST'] = POST
        else:
            message['Allow'].remove('POST')
            message['Allow'].append('PATCH')
            message['Allow'].append('DELETE')
        self.set_status(200)
        self.finish(message)