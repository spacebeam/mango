# -*- coding: utf-8 -*-
'''
    Mango HTTP tasks handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import time
import arrow
import motor

import logging

# import numpy as np
import pandas as pd

from bson import json_util

from tornado import gen
from tornado import web

from mango.system import accounts
from mango.system import tasks

from mango.tools import content_type_validation
from mango.tools import check_json
from mango.tools import check_times
from mango.tools import errors
from mango.tools import new_resource

from mango.handlers import BaseHandler


@content_type_validation
class Handler(tasks.Tasks, accounts.Accounts, BaseHandler):
    '''
        Tasks HTTP request handlers
    '''

    @gen.coroutine
    def get(self, task_uuid=None, start=None, end=None, page_num=0, lapse='hours'):
        '''
            Get tasks handler
        '''

        # -- logging info

        logging.warning('daaaa fuck1!!{0}'.format(task_uuid))

        logging.info(self.request.arguments)

        #account = (self.request.arguments.get('account', [None])[0] if not account else account)

        # query string checked from string to boolean
        #checked = str2bool(str(self.request.arguments.get('checked', [False])[0]))

        if task_uuid:
            task_uuid = task_uuid.rstrip('/')

            if self.current_user:
                user = self.current_user
                task = yield self.get_task(user, task_uuid)
            else:
                task = yield self.get_task(None, task_uuid)

            if not task:
                self.set_status(400)
                system_error = errors.Error('missing')
                error = system_error.missing('task', task_uuid)
                self.finish(error)
                return

            self.finish(task)
            return

        if self.current_user:
            user = self.current_user
            orgs = yield self.get_orgs_list(user)
            
            account_list = (orgs['orgs'] if orgs else False)
            if not account_list:
                result = yield self.get_task_list(
                                        account=user, 
                                        lapse=lapse,
                                        start=start,
                                        end=end,
                                        page_num=page_num)
            else:
                account_list.append(user)
                result = yield self.get_task_list(
                                        account=account_list,
                                        lapse=lapse,
                                        start=start,
                                        end=end,
                                        page_num=page_num)
        else:
            result = yield self.get_task_list(
                                    account=None,
                                    lapse=lapse,
                                    start=start,
                                    end=end,
                                    page_num=page_num)

        result = json_util.dumps(result)

        self.finish(result)

    @gen.coroutine
    def post(self):
        '''
            POST tasks handler
        '''
        struct = yield check_json(self.request.body)
        db = self.settings['db']
        
        format_pass = (True if struct else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return

        task = yield self.new_task(struct)
 
        if not task:
            model = 'Tasks'
            error = {'task':False}
            reason = {'duplicates':[('Task', 'uniqueid'), (model, 'uuid')]}

            message = yield self.let_it_crash(struct, model, error, reason)

            self.set_status(400)
            self.finish(message)
            return
        
        if 'accountcode' in struct:

            account = struct.get('accountcode')

            resource = {
                'account': account,
                'resource':'tasks',
                'uuid':task
            }

            exist = yield self.check_exist(account)

            logging.info('check if exist %s ' % exist)

            if exist:
                update = yield new_resource(db, resource)

                logging.info('update %s' % update)

                flag = yield self.set_assigned_flag(account, task)

        logging.info('new spawned task %s ' % task)

        self.set_status(201)
        self.finish({'uuid':task})

    ##@web.authenticated
    @gen.coroutine
    def put(self):
        '''
            Put tasks handler
        '''
        pass

    ##@web.authenticated
    @gen.coroutine
    def delete(self, task_uuid):
        '''
            Delete tasks handler
        '''
        task_uuid = task_uuid.rstrip('/')
        result = yield self.remove_task(task_uuid)

        if not result['n']:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('task', task_uuid)
            self.finish(error)
            return

        self.set_status(204)
        self.finish()

    ##@web.authenticated
    @gen.coroutine
    def patch(self):
        '''
            Patch tasks handler
        '''
        pass


@content_type_validation
class PublicHandler(tasks.Tasks, BaseHandler):
    '''
        Mango public tasks handler
        
        Public tasks handler
    '''
    
    @gen.coroutine
    def get(self, page_num=0):
        '''
            Get public handler
        '''
        # get public details: task get_task_list without an account
        account = None
        result = yield self.get_task_list(account=account,
                                            lapse=None,
                                            start=None,
                                            end=None,
                                            page_num=page_num)
        
        self.finish({'results': result})


@content_type_validation
class UnassignedHandler(tasks.Tasks, BaseHandler):
    '''
        Unassigned requests handler
    '''
    
    @gen.coroutine
    def get(self, page_num=0):
        '''
            Get unassigned handler
        '''
        result = yield self.get_unassigned_tasks(lapse=None,
                                                   start=None,
                                                   end=None,
                                                   page_num=page_num)
        self.finish(result)