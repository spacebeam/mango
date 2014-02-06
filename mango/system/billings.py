# -*- coding: utf-8 -*-
'''
    Mango billings system logic.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import arrow
import motor

# import numpy as np
import pandas as pd


from tornado import gen



class Billings(object):
    '''
        Billings resources
    '''
   
    @gen.engine 
    def get_cost_summary(self, account, routes, lapse, start, stop, callback):
        '''
            get_cost_summary
        '''

        if not start:
            start = arrow.utcnow()
        if not stop:
            stop = start.replace(days=+1)

        start = start.timestamp

        # TODO: multiple routes
        single_route = routes

        # MongoDB aggregation match operator
        if type(account) is list:
            match = {
                'assigned':True,
                'start':{'$gte':start, '$lt':stop},
                'channel': {'$regex': single_route['channel']},
                'dstchannel': {'$regex': single_route['dstchannel']},
                '$or':[{'accountcode':a} for a in account]
            }
        else:
            match = {
                'accountcode':account, 
                'assigned': True,
                'start': {'$gte':start, '$lt': stop},
                'channel': {'$regex': single_route['channel']},
                'dstchannel': {'$regex': single_route['dstchannel']},
            }
    
        # MongoDB aggregation project operator
        project = {
               "_id" : 0,
               # record duration seconds
               "duration" : 1,
               # record billing seconds
               "billsec" : 1,
               # record times
               "start" : 1,
               'answer':1,
               'end':1,
        
               "year" : {
                         "$year" : "$start"
               },
               "month" : {
                          "$month" : "$start"
               },
               "week" : {
                         "$week" : "$start"
               },
               "day" : {  
                        "$dayOfMonth" : "$start"
               },
               "hour" : {  
                         "$hour" : "$start"
               },
               "minute" : {  
                           "$minute" : "$start"
               },
               "second" : {
                           "$second" : "$start"
               }
        }
        
        # MongoDB aggregation group operator
        group = {
            '_id': {
                'start': '$start',
                'answer': '$answer',
                'end': '$end',
                
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
            'billsecs': {
                '$sum':'$billsec'
            }
        }
        
        # MongoDB aggregation pipeline
        pipeline = [
            {'$match':match},
            {'$project':project},
            {'$group':group}
        ]
        
        try:
            result = yield motor.Op(self.db.records.aggregate, pipeline)
            
        except Exception, e:
            callback(None, e)
            return
        
        callback(result['result'], None)