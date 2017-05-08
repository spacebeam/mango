# -*- coding: utf-8 -*-
'''
    Mango tools system periodic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'

import logging
from tornado import httpclient
import ujson as json
import uuid
import urllib
from tornado import gen


httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')


@gen.coroutine
def get_coturn_tasks(db):
    '''
        Get coturn label tasks
    '''
    tasks_list = []
    try:
        query = db.tasks.find(
            {'label':'coturn',
             'assigned': False}, 
            {'_id':0} # 'account':1, 'uuid':1,
        )
        while (yield query.fetch_next):
            task = query.next_object()
            tasks_list.append(task)
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)

    raise gen.Return(tasks_list)

@gen.coroutine
def get_raw_records(sql, query_limit):
    '''
        Get RAW records
    '''
    http_client = httpclient.AsyncHTTPClient()
    # handle restuff callback actions
    def handle_restuff(response):
        '''
            Request Handler Restuff
        '''
        if response.error:
            logging.error(response.error)
        else:
            logging.info(response.body)
    # handle request callback actions
    def handle_request(response):
        '''
            Request Handler
        '''
        if response.error:
            logging.error(response.error)
        else:
            res = json.loads(response.body)
            request_id = res.get('uuid', None)
            if request_id:
                request_id = request_id.get('uuid')
            # requests
            http_client.fetch(
                'http://iofun.io/records/{0}'.format(request_id), 
                headers={"Content-Type": "application/json"},
                method='GET',
                #body=json.dumps(record),
                callback=handle_restuff
            )
            # if successful response we need to send ack now to sql
            # and mack the flag of that call as checked, otherwise
            # we need some other type of validation.
    try:
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
            WHERE checked = false
            ORDER BY uniqueid DESC
            LIMIT {0};
        '''.format(
            query_limit
        )
        result = yield sql.query(query)
        if result:
            for row in result:
                record = dict(row.items())
                http_client.fetch(
                    'http://iofun.io/records/', 
                    headers={"Content-Type": "application/json"},
                    method='POST',
                    body=json.dumps(record),
                    callback=handle_request
                )
            message = {'ack': True}
        else:
            message = {'ack': False}
        result.free()
    except Exception, e:
        logging.exception(e)
        raise e
    raise gen.Return(message)

@gen.coroutine
def checked_flag(sql, uniqueid):
    '''
        periodic checked flag
    '''
    message = False
    try:
        query = '''
            UPDATE cdr set checked = true where uniqueid = '{0}'
        '''.format(uniqueid)
        result = yield sql.query(query)
        if len(result) > 0:
            message = True
        result.free()
    except Exception, e:
        logging.exception(e)
        raise e

    raise gen.Return(message)

@gen.coroutine
def get_query_records(sql, query_limit):
    '''
        periodic query records function
    '''
    record_list = []
    http_client = httpclient.AsyncHTTPClient()
    # handle record uuid
    def handle_record_uuid(response):
        '''
            Request Handler Record UUID
        '''
        if response.error:
            logging.error(response.error)
        else:
            logging.info(response.body)
    # handle request
    def handle_request(response):
        '''
            Request Handler
        '''
        if response.error:
            logging.error(response.error)
        else:
            result = json.loads(response.body)
            request_id = result.get('uuid', None)
            if request_id:
                request_id = request_id.get('uuid')
            http_client.fetch(
                'http://iofun.io/records/{0}'.format(request_id), 
                headers={"Content-Type": "application/json"},
                method='GET',
                callback=handle_record_uuid
            )
    try:
        # Get SQL database from system settings
        # PostgreSQL insert new sip account query
        query = '''
            SELECT
                DISTINCT ON (uniqueid) uniqueid,
                start,
                date(start) as strdate,
                clid as callerid,
                src as source,
                dst as destination,
                dcontext as destination_context,
                channel,
                dstchannel as destination_channel,
                duration,
                billsec,
                billsec as seconds,
                disposition,
                checked 
            FROM cdr 
            WHERE checked = false
            ORDER BY uniqueid DESC
            LIMIT {0};
        '''.format(
            query_limit
        )
        result = yield sql.query(query)
        for x in result:
            record_list.append(x)
        result.free()
    except Exception, e:
        logging.exception(e)
        raise e
    raise gen.Return(record_list)