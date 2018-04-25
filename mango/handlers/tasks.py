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
from mango.tools import str2bool, check_json
from mango.handlers import BaseHandler
from collections import OrderedDict


class Handler(tasks.Tasks, BaseHandler):
    '''
        HTTP request handlers
    '''

    @gen.coroutine
    def head(self,
             account=None,
             task_uuid=None,
             start=None,
             end=None,
             lapse='hours',
             page_num=1):
        '''
            Get tasks
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend username from token
        username = self.get_username_token()
        # if the user don't provide an account we use the username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # rage against the finite state machine
        status = 'all'
        # init message on error
        message = {'error':True}
        # init status that match with our message
        self.set_status(400)
        # check if we're list processing
        if not task_uuid:
            message = yield self.get_task_list(account,
                                               start,
                                               end,
                                               lapse,
                                               status,
                                               page_num)
            self.set_status(200)
        # single task received
        else:
            # first try to get stuff from cache
            task_uuid = task_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('tasks:{0}'.format(task_uuid))
            if message is not None:
                logging.info('tasks:{0} done retrieving!'.format(task_uuid))
                self.set_status(200)
            else:
                message = yield self.get_task(account, task_uuid)
                if self.cache.add('tasks:{0}'.format(task_uuid), message, 1):
                    logging.info('new cache entry {0}'.format(str(task_uuid)))
                    self.set_status(200)
        # so long and thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def get(self,
            account=None,
            task_uuid=None,
            start=None,
            end=None,
            lapse='hours',
            page_num=1):
        '''
            Get tasks
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend username from token
        username = self.get_username_token()
        # if the user don't provide an account we use the username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])

        search = (query_args.get('search', [search])[0] if not search else search)
        
        # rage against the finite state machine
        status = 'all'
        # init message on error
        message = {'error':True}
        # init status that match with our message
        self.set_status(400)
        # check if we're list processing
        if not task_uuid and search:
            message = yield self.quick_search(account, start, end, lapse, status, page_num, fields, search)
            self.set_status(200)
        elif not task_uuid:
            message = yield self.get_task_list(account,
                                               start,
                                               end,
                                               lapse,
                                               status,
                                               page_num)
            self.set_status(200)
        # single task received
        else:
            # first try to get stuff from cache
            task_uuid = task_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('tasks:{0}'.format(task_uuid))
            if message is not None:
                logging.info('tasks:{0} done retrieving!'.format(task_uuid))
                self.set_status(200)
            else:
                message = yield self.get_task(account, task_uuid)
                if self.cache.add('tasks:{0}'.format(task_uuid), message, 1):
                    logging.info('new cache entry {0}'.format(str(task_uuid)))
                    self.set_status(200)
        # so long and thanks for all the fish
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
        # get the current frontend username from token
        username = self.get_username_token()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # execute new task struct
        task_uuid = yield self.new_task(struct)
        # complete message with receive uuid.
        message = {'uuid':task_uuid}
        if 'error' in message['uuid']:
            scheme = 'task'
            reason = {'duplicates': [
                (scheme, 'account'),
                (scheme, 'uuid')
            ]}
            message = yield self.let_it_crash(struct, scheme, message['uuid'], reason)
            self.set_status(400)
        else:
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
        # remove query string flag
        remove = self.request.arguments.get('remove', False)
        if not remove :
            result = yield self.modify_task(account, task_uuid, struct)
        else:
            result = yield self.modify_remove(account, task_uuid, struct)
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
            else:
                parameters[k] = str(type(v))
        # after automatic madness return description and parameters
        parameters['labels'] = 'array/string'
        # end of manual cleaning
        POST = {
            "description": "Create task",
            "parameters": OrderedDict(sorted(parameters.items(), key=lambda t: t[0]))
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
