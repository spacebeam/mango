# -*- coding: utf-8 -*-
'''
    Mango system periodic tools.
'''

# This file is part of mango.

# Dist4ributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'

import logging
from tornado import httpclient
import ujson as json
import urllib
import motor
import queries

from contextlib import contextmanager
from tornado import gen

# from mango.messages import accounts

from bson import objectid


@gen.coroutine
def get_raw_records(sql, query_limit):
    '''
        Get RAW records
    '''
    httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
    http_client = httpclient.AsyncHTTPClient()

    def handle_restuff(response):
        '''
            Request Handler
        '''
        print 'yeahaha'
        if response.error:
            logging.error(response.error)
        else:
            logging.info(response.body)

    def handle_request(response):
        '''
            Request Handler
        '''
        if response.error:
            logging.error(response.error)
        else:

            logging.info(response.body)

            res = json.loads(response.body)

            logging.info(res.get('uuid', None))

            http_client.fetch(
                'http://127.0.0.1/records/' + res.get('uuid'), 
                headers={"Content-Type": "application/json"},
                method='GET',
                #body=json.dumps(record),
                callback=handle_restuff
            )

            # if successful response we need to send ack now to sql
            # and mack the flag of that call as checked, otherwise
            # we need some othe type of validation.

    try:
        # Get SQL database from mango settings
        query = '''
            SELECT
                DISTINCT ON (uniqueid) uniqueid,
                src as source,
                dst as destination,
                dcontext,
                channel,
                dstchannel,
                lastapp,
                lastdata,
                duration,
                billsec,
                disposition,
                checked

            FROM cdr

            ORDER BY uniqueid DESC

            limit {0};
        '''.format(
            query_limit
        )
        result = yield sql.query(query)

        if result:

            for row in result:

                record = dict(row.items())

                http_client.fetch(
                    'http://127.0.0.1/records/', 
                    headers={"Content-Type": "application/json"},
                    method='POST',
                    body=json.dumps(record),
                    callback=handle_request
                )

            message = {'ack': True}
        else:
            message = {'ack': False}

        result.free()

        logging.warning('get raw records spawned on PostgreSQL {0}'.format(message))
        
    except Exception, e:
        logging.exception(e)
        raise e

    raise gen.Return(message)

@gen.coroutine
def get_usernames(db):
    '''
        Get all the username accounts
    '''
    usernames = []
    try:
        query = db.accounts.find(
            {}, 
            {'account':1, 'uuid':1, '_id':0}
        )
        while (yield query.fetch_next):
            account = query.next_object()
            usernames.append(account)
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)

    raise gen.Return(usernames)

@gen.coroutine
def get_unassigned_call(db):
    '''
        Get 'one thousand' unassigned calls.
    '''
    try:
        result = []

        query = db.calls.find({
            'assigned': {
                '$exists': False
            }
        }).limit(800)
        
        for call in (yield query.to_list()):
            result.append(call)
            
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)
    
    raise ren.Return(result)

@gen.coroutine
def process_assigned_false(db):
    '''
        Periodic task that process 'one thousand' 
        assigned False flag on calls resource.
    '''

    result = []

    def _got_call(message, error):
        '''
            got call
        '''
        if message:
            channel = (message['channel'] if 'channel' in message else False)

            if channel:
                account = [a for a in _account_list 
                           if ''.join(('/', a['account'], '-')) in channel]

                account = (account[0] if account else False)

                if account:
                    struct = {
                        'account':account['account'],
                        'resource':'calls',
                        'id':message['_id']
                    }
                    result.append(struct)
        elif error:
            logging.error(error)
            return error
        else:
            #logging.info('got call result: %s', result)
            return result
    try:
        _account_list = yield get_usernames(db)

        db.calls.find({
            'assigned':False
        }).limit(800).each(_got_call)
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)

@gen.coroutine
def process_assigned_records(db):
    '''
        Periodic task that process 'one thousand' 
        unassigned calls resource.
    '''
    result = []

    def _got_record(message, error):
        '''
            got record
        '''
        if error:
            logging.error(error)
            return error

        elif message:
            channel = (True if 'channel' in message else False)
            # get channel the value
            channel = (message['channel'] if channel else channel)

            if channel:
                account = [a for a in _account_list
                           if ''.join(('/', a['account'], '-')) in channel]
                account = (account[0] if account else False)

                if account:
                    struct = {
                        'account':account['account'],
                        'resource':'calls',
                        'id':message['_id']
                    }
                    result.append(struct)    
        else:
            #logging.info('got record result: %s', result)
            return result

    try:
        _account_list = yield get_usernames(db)

        db.calls.find({
            'assigned':{'$exists':False}
        }).limit(800).each(_got_record)
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)

@gen.coroutine
def assign_record(db, account, callid):
    '''
        Update record assigned flag
    '''
    try:
        result = yield db.calls.update(
            {'_id':objectid.ObjectId(callid)}, 
            {'$set': {'assigned': True,
                      'accountcode':account}}
        )

    except Exception, e:
        logging.exception(e)
        raise e

        return

    raise gen.Return(result)

@gen.coroutine
def records_callback(sql):
    '''
        periodic records callback
    '''
    logging.info('a little brain dead')

    try:
        # Get SQL database from system settings
        # PostgreSQL insert new sip account query
        query = '''
            SELECT DISTINCT uniqueid, 
                   date(calldate),
                   src as source,
                   dst as destination,
                   sum(billsec) as seconds,
                   CASE 
                       WHEN checked IS NULL 
                       THEN 'False' 
                       ELSE 'True' 
                   END AS has_profile 
            FROM cdr WHERE date(calldate) = '2015-07-23' and dstchannel like 'SIP/ticolinea_0%'
            GROUP by uniqueid, date, src, destination, checked 
            ORDER by uniqueid;
        '''#.format(
            #struct.get('account'),
            #struct.get('account'),
            #struct.get('account'),
            #struct.get('domain', self.settings.get('domain')),
            #struct.get('password')
        #)
        result = yield sql.query(query)

        rows = len(result)

        for x in result:
            logging.info(x)

        if result:
            message = {'ack': True}
        else:
            message = {'ack': False}

        result.free()

        logging.warning('{0} rows spawned on {1} {2}'.format(rows, 'mango', 'ack missing'))

        # TODO: Still need to check the follings exceptions with the new queries module.
        #except (psycopg2.Warning, psycopg2.Error) as e:
        #    logging.exception(e)
        #    raise e
        
    except Exception, e:
        logging.exception(e)
        raise e

    raise gen.Return(message)