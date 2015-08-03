# -*- coding: utf-8 -*-
'''
    Mango records system logic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import logging

import arrow
import motor

import uuid

# import numpy as np
import pandas as pd

from tornado import gen

from mango.messages import records
from mango.messages import reports

from mango.tools import clean_structure
from mango.tools import clean_results
from mango.tools import check_times


class Records(object):
    '''
        Records resources
    '''

    @gen.coroutine
    def get_record(self, account, record_uuid):
        '''
            Get a detail record
        '''
        message = 'where is this account {0} record {1}'.format(account, record_uuid)
        logging.info(message)
        if not account:
            record = yield self.db.records.find_one({'uuid':record_uuid}, {'_id':0})
        else:

            # change accountcode to account, because the accountcode is a uuid
            # and we're expecting an account name.
            message = 'account {0} and record {1} are you for real?'.format(account, record_uuid)
            logging.info(message)

            record = yield self.db.records.find_one({'uuid':record_uuid,
                                                     'account':account},
                                                    {'_id':0})
            logging.info(record)
        try:
            if record:
                record = records.Record(record)
                record.validate()

                record = clean_structure(record)
        except Exception, e:
            logging.exception(e) # catch some daemon here!
            raise e
        finally:
            raise gen.Return(record)

    @gen.coroutine
    def get_record_list(self, account, start, end, lapse, page_num):
        '''
            Get detail records 
        '''
        message = 'where are the records for this account {0} page {1}'.format(account, page_num)
        logging.info(message)
        page_num = int(page_num)
        page_size = self.settings['page_size']
        record_list = []
        
        if not account:
            query = self.db.records.find({'public':False}, {'_id':0})
        elif type(account) is list:
            accounts = [{'accountcode':a, 'assigned': True} for a in account]
            query = self.db.records.find({'$or':accounts})
        else:
            query = self.db.records.find({'accountcode':account,
                                        'assigned':True})
        
        query = query.sort([('uuid', -1)]).skip(page_num * page_size).limit(page_size)
        
        try:
            
            while (yield query.fetch_next):
                result = query.next_object()
                record_list.append(records.Record(result))

        except Exception, e:
            logging.exception(e)
            raise e

        try:
            struct = {'results': record_list}
            message = reports.BaseResult(struct)
            message.validate()
            message = clean_results(message)
        except Exception, e:
            logging.exception(e)
            raise e
        finally:
            raise gen.Return(message)
    
    @gen.coroutine
    def get_unassigned_records(self, start, end, lapse, page_num):
        '''
            Get unassigned record detail records
        '''
        page_num = int(page_num)
        page_size = self.settings['page_size']
        result = []
        
        # or $exist = false ?

        query = self.db.records.find({'assigned':False})
        query = query.sort([('uuid', -1)]).skip(page_num * page_size).limit(page_size)
        
        try:
            for record in (yield query.to_list()):
                result.append(records.Record(record))
            
            struct = {'results':result}

            results = reports.BaseResult(struct)
            results.validate()
        except Exception, e:
            logging.exception(e)
            raise e

        results = clean_results(results)        
        raise gen.Return(results)


    @gen.coroutine
    def get_summaries(self, account, start, end, lapse, page_num):
        '''
            Get summaries
        '''
        times = yield check_times(start, end)

        if lapse:
            logging.info('get summaries lapse %s' % (lapse))

    @gen.coroutine
    def get_summary(self, account, start, end, lapse):
        '''
            Get summary
        '''
        
        times = yield check_times(start, end)

        logging.info('Get summary for {0} lapse {1} start period {2} end period {3}'.format(
            account, lapse, start, end
        ))

        # MongoDB aggregation match operator
        if type(account) is list:
            match = {
                'assigned':True,
                'start':{'$gte':times.get('start'), '$lt':times.get('end')},
                '$or':[{'accountcode':a} for a in account]
            }
        else:
            match = {
                'accountcode':account, 
                'assigned': True,
                'start': {'$gte':times.get('start'), '$lt': times.get('end')}
            }

        if not account:
            logging.info('not account')
            match = {
                'public': False
            }

        #  month : { $month : ISODate(localHitDate) }

        # MongoDB aggregation project operator
        project = {
            "_id" : 0,
            
            # record timestamps
            "start":1,
            #"answer":1,
            #"end":1,
            
            # record duration seconds
            "duration" : 1,
            # record billing seconds
            "billsec" : 1,
            
            # project id's timestamp stuff?
            "year" : {  
                "$year" : "ISODate(start)"
            },
            "month" : {  
                "$month" : "ISODate(start)"
            },
            "week" : {  
                "$week" : "ISODate(start)"
            },
            "day" : {
                "$dayOfMonth" : "ISODate(start)"
            },
            "hour" : {
                "$hour" : "ISODate(start)"
            },
            "minute" : {
                "$minute" : "ISODate(start)"
            },
            "second" : {
                "$second" : "ISODate(start)"
            }
        }

        # MongoDB aggregation group operator

        # R&D on group by accountcode, account, uuid, or something else ...

        group = {
            '_id': {
                'start': 'ISODate($start)',
                #'answer': '$answer',
                #'end': '$end',
                'year': '$year',
                'month': '$month',
                'week':'$week',
                'day': '$day',
                'hour':'$hour',
                'minute': '$minute',
                'second': '$second',
            },

            'records': {
                '$sum':1
            },

            'average': {
                '$avg':'$billsec'
            },

            'duration': {
                '$sum':'$duration'
            },

            'billing': {
                '$sum':'$billsec'
            }
        }

        # MongoDB aggregation pipeline
        pipeline = [
            {'$match':match},
            {'$project':project},
            {'$group':group}
        ]

        result = yield self.db.records.aggregate(pipeline)

        raise gen.Return(result.get('result'))

    @gen.coroutine
    def new_detail_record(self, struct, db=None):
        '''
            Create a new record entry
        '''
        if not db:
            db = self.db
        try:
            # if not type str convert to str...
            # same note different day... WTF I'm talking about...

            if isinstance(struct, dict):

                struct['strdate'] = '"{0}"'.format(struct.get('strdate', ''))
            
            record = records.Record(struct)
            record.validate()
        except Exception, e:
            logging.exception(e)
            raise e

        record = clean_structure(record)

        result = yield db.records.insert(record)

        message = {
            'uniqueid':struct.get('uniqueid'),
            'uuid':record.get('uuid')
        }

        raise gen.Return(message)

    @gen.coroutine
    def set_assigned_flag(self, account, record_uuid):
        '''
            Set the record assigned flag
        '''
        logging.info('set_assigned_flag account: %s, record: %s' % (account, record_uuid))

        result = yield self.db.records.update(
                                {'uuid':record_uuid, 
                                 'accountcode':account}, 
                                {'$set': {'assigned': True}})
        
        raise gen.Return(result)

    @gen.coroutine
    def remove_record(self, record_uuid):
        '''
            Remove a record entry
        '''
        result = yield self.db.records.remove({'uuid':record_uuid})
        raise gen.Return(result)

    @gen.coroutine
    def replace_record(self, struct):
        '''
            Replace a existent record entry
        '''
        # put implementation
        pass

    @gen.coroutine
    def resource_options(self):
        '''
            Return resource options
        '''
        # options implementation
        pass

    @gen.coroutine
    def modify_record(self, struct):
        '''
            Modify a existent record entry
        '''
        # patch implementation
        pass