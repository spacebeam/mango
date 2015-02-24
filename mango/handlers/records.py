# -*- coding: utf-8 -*-
'''
    Mango HTTP records handlers.
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
from mango.system import records

from mango.tools import content_type_validation
from mango.tools import check_json
from mango.tools import check_times
from mango.tools import errors
from mango.tools import new_resource

from mango.handlers import BaseHandler


@content_type_validation
class Handler(records.Records, accounts.Accounts, BaseHandler):
    '''
        Records HTTP request handlers
    '''

    @gen.coroutine
    def get(self, record_uuid=None, start=None, end=None, page_num=0, lapse='hours'):
        '''
            Get records handler
        '''

        # -- logging info

        logging.info(self.request.arguments)

        #account = (self.request.arguments.get('account', [None])[0] if not account else account)

        # query string checked from string to boolean
        #checked = str2bool(str(self.request.arguments.get('checked', [False])[0]))

        if record_uuid:
            record_uuid = record_uuid.rstrip('/')

            if self.current_user:
                user = self.current_user
                record = yield self.get_record(user, record_uuid)
            else:
                record = yield self.get_record(None, record_uuid)

            if not record:
                self.set_status(400)
                system_error = errors.Error('missing')
                error = system_error.missing('record', record_uuid)
                self.finish(error)
                return

            self.finish(record)
            return

        if self.current_user:
            user = self.current_user
            orgs = yield self.get_orgs_list(user)
            
            account_list = (orgs['orgs'] if orgs else False)
            if not account_list:
                result = yield self.get_record_list(
                                        account=user, 
                                        lapse=lapse,
                                        start=start,
                                        end=end,
                                        page_num=page_num)
            else:
                account_list.append(user)
                result = yield self.get_record_list(
                                        account=account_list,
                                        lapse=lapse,
                                        start=start,
                                        end=end,
                                        page_num=page_num)
        else:
            result = yield self.get_record_list(
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
            Post records handler
        '''
        struct = yield check_json(self.request.body)
        db = self.settings['db']
        
        format_pass = (True if struct else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return

        record = yield self.new_detail_record(struct)
 
        if not record:
            model = 'Records'
            error = {'record':False}
            reason = {'duplicates':[('Record', 'uniqueid'), (model, 'uuid')]}

            message = yield self.let_it_crash(struct, model, error, reason)

            self.set_status(400)
            self.finish(message)
            return
        
        if 'accountcode' in struct:

            account = struct.get('accountcode')

            resource = {
                'account': account,
                'resource':'records',
                'uuid':record
            }

            exist = yield self.check_exist(account)

            logging.info('check if exist %s ' % exist)

            if exist:
                update = yield new_resource(db, resource)

                logging.info('update %s' % update)

                flag = yield self.set_assigned_flag(account, record)

        logging.info('new spawned record %s ' % record)

        self.set_status(201)
        self.finish({'uuid':record})

    ##@web.authenticated
    @gen.coroutine
    def put(self):
        '''
            Put records handler
        '''
        pass

    ##@web.authenticated
    @gen.coroutine
    def delete(self, record_uuid):
        '''
            Delete records handler
        '''
        record_uuid = record_uuid.rstrip('/')
        result = yield self.remove_record(record_uuid)

        if not result['n']:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('record', record_uuid)
            self.finish(error)
            return

        self.set_status(204)
        self.finish()

    ##@web.authenticated
    @gen.coroutine
    def patch(self):
        '''
            Patch records handler
        '''
        pass


@content_type_validation
class PublicHandler(records.Records, BaseHandler):
    '''
        Mango public records handler
        
        Public records handler
    '''
    
    @gen.coroutine
    def get(self, page_num=0):
        '''
            Get public handler
        '''
        # get public details: record get_record_list without an account
        account = None
        result = yield self.get_record_list(account=account,
                                            lapse=None,
                                            start=None,
                                            end=None,
                                            page_num=page_num)
        
        self.finish({'results': result})


@content_type_validation
class UnassignedHandler(records.Records, BaseHandler):
    '''
        Unassigned requests handler
    '''
    
    @gen.coroutine
    def get(self, page_num=0):
        '''
            Get unassigned handler
        '''
        result = yield self.get_unassigned_records(lapse=None,
                                                   start=None,
                                                   end=None,
                                                   page_num=page_num)
        self.finish(result)


@content_type_validation
class SummaryHandler(records.Records, accounts.Accounts, BaseHandler):
    '''
        Summary requests handler 
    '''
    ###@web.authenticated
    @gen.coroutine
    def get(self, account=None, start=None, end=None, lapse='hours', page_num=0):
        '''
            Get record summary

            arguments: account, start, end, lapse, page.

            - account or list of accounts
            - start timestamp
            - end timestamp
            - lapse of time
            - page number
        '''
        result = 0
        minutes = 0
        record_avg = 0

        if not account:
            account = self.current_user

        orgs = yield self.get_orgs_list(account)
        account_list = (orgs['orgs'] if orgs else False)

        if account_list:
            account_list.append(account)
            summary = yield self.get_summary(account=accounts,
                                             start=start,
                                             end=end,
                                             lapse=lapse)
        else:
            summary = yield self.get_summary(account=account,
                                             start=start,
                                             end=end,
                                             lapse=lapse)

        if summary:

            # remove from query

            dates = [record['_id'] for record in summary]
            
            for _x in summary:
                del _x['_id']
            
            frame = pd.DataFrame(summary)
            frame = frame.join(pd.DataFrame(dates))
        
            if lapse:
                lapse = lapse.rstrip('/')

                if 'hours' in lapse:
                    # pandas data-frames
                    frame['minutes'] = frame['billsecs'] / 60
                    
                    # research pandas dataframe set_index
                    hours = frame[['records', 'minutes', 'start']].groupby('start').sum()
                    
                    # get a dict of results from the data-frame
                    result =  dict(hours['records'])
                    minutes = dict(hours['minutes'])
                    
                    result = {         
                        time.mktime(key.timetuple()): int(result[key]) 
                        for key in result
                    }            
                    
                    minutes = {
                        time.mktime(key.timetuple()): int(minutes[key])
                        for key in minutes
                    } 
                                        
                    # return the clean version of the data
                    self.finish({
                        'records': result, 
                        'minutes': minutes
                    })

                    return
            
            result = frame['records'].sum()
            seconds = frame['billsecs'].sum()
            average = frame['average'].sum()
        
            minutes = seconds / 60
            min_avg = average / 60
            
            record_avg = round(min_avg / result)
        
        self.finish({'records': int(result),
                     'minutes': int(minutes),
                     'record_avg': int(record_avg)})


@content_type_validation
class SummariesHandler(records.Records, accounts.Accounts, BaseHandler):
    '''
       Summaries requests handler.
    '''
    
    ###@web.authenticated
    @gen.coroutine
    def get(self, account=None, start=None, end=None, lapse=None, page_num=0):
        '''
            Get summaries handler
        '''
        message = {}
        result = None
        minutes = 0
        record_avg = 0

        times = yield check_times(start, end)

        if not account:
            account = self.current_user

        orgs = yield self.get_orgs_list(account)
        account_list = (orgs['orgs'] if orgs else False)

        if account_list:
            account_list.append(account)
            summary = yield self.get_summary(
                account=account_list,
                lapse=lapse,
                start=times.get('start'),
                end=times.get('end')
            )
        else:
            summary = yield self.get_summary(account=account,
                                             lapse=lapse,
                                             start=times['start'],
                                             end=times['end'])
        if summary:

            logging.warning("remove record.get('_id') %s from query" % (record.get('_id')))
            
            dates = [record['_id'] for record in summary]
            
            for x in summary:
                del x['_id']
            
            frame = pd.DataFrame(summary)
            frame = frame.join(pd.DataFrame(dates))
        
            if lapse:
                lapse = lapse.rstrip('/')

                logging.info('time lapse on summaries: %s' % lapse)
            
                if 'hours' in lapse:
                    # pandas data-frames
                    frame['minutes'] = frame['billsecs'] / 60
                    
                    # research pandas dataframe set_index
                    hours = frame[['records', 'minutes', 'start']].groupby('start').sum()
                    
                    # get a dict of results from the data-frame
                    result =  dict(hours['records'])
                    minutes = dict(hours['minutes'])
                    
                    result = {         
                        time.mktime(key.timetuple()): int(result[key]) 
                        for key in result
                    }            
                    
                    minutes = {
                        time.mktime(key.timetuple()): int(minutes[key])
                        for key in minutes
                    } 
                                        
                    # return the clean version of the data
                    self.finish({
                        'records': result, 
                        'minutes': minutes
                    })
                    return
            
            result = frame['result'].sum()
            seconds = frame['billsecs'].sum()
            average = frame['average'].sum()
        
            minutes = seconds / 60
            min_avg = average / 60
            
            record_avg = round(min_avg / result)
        
        self.finish({'records': int(result),
                     'minutes': int(minutes),
                     'record_avg': int(record_avg)})