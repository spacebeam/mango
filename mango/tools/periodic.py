# -*- coding: utf-8 -*-
'''
    Mango system periodic tools.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import motor

from contextlib import contextmanager
from tornado import gen

# from mango.messages import accounts

from bson import objectid


@gen.coroutine
def get_usernames(db):
    '''
        Mango get usernames
        
        Get all the usernames
    '''
    
    # limit the size of the find query.

    usernames = []
    try:
        query = db.accounts.find({},{'account':1, '_id':0})
        
        for a in (yield query.to_list()):
            usernames.append(a)
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)
    
    raise gen.Return(usernames)

@gen.coroutine
def get_unassigned_cdr(db):
    '''

        Get unassigned CDR.
    '''
    try:
        result = []

        query = db.calls.find({'assigned':{'$exists':False}}).limit(1000)
        
        for c in (yield query.to_list()):
            result.append(c)
            
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)
    
    raise ren.Return(result)

@gen.coroutine
def process_assigned_false(db):
    '''
        lol this is fucking nonsense
        ----------------------------

        Periodic task to process assigned false
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
            #logging.exception(error)
            raise gen.Return(error)
            return
        else:
            raise gen.Return(result)
            return
    try:
        _account_list = yield get_usernames(db)

        db.calls.find({
            'assigned':False
        }).limit(1000).each(_got_call)
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)

@gen.coroutine
def process_assigned_records(db):
    '''
        Periodic task that process unassigned records.
    '''
    result = []

    def _got_record(message, error):
        '''
            got record
        '''
        if error:
            raise gen.Return(error)
            return

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
            raise gen.Return(result)
            return

    try:
        _account_list = yield get_usernames(db)

        db.calls.find({
            'assigned':{'$exists':False}
        }).limit(1000).each(_got_record)
    except Exception, e:
        logging.exception(e)
        raise gen.Return(e)

@gen.coroutine
def assign_call(db, account, callid):
    '''
        Update call assign flag
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