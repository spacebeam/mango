#!/usr/bin/env python
'''
    Mango periodic tools
'''
from contextlib import contextmanager
from tornado import gen
from mango.models import accounts
from bson import objectid
import motor


@gen.engine
def get_usernames(db, callback):
    '''
        Mango get usernames
        
        Get all the usernames
    '''
    usernames = []
    try:
        query = db.accounts.find({},{'account':1, '_id':0})
        
        for a in (yield motor.Op(query.to_list)):
            usernames.append(a)
    except Exception, e:
        callback(None, e)
    
    callback(usernames, None)


@gen.engine
def new_resource_context(db, struct, callback):
    '''
        Mango new resource context

        Create a new account resource
    '''
    try:
        res = accounts.AccountResource(**struct).validate()
    except Exception, e:
        callback(None, e)
        return
    
    resource = ''.join(('resources.', res['resource']))
    
    try:
        result = yield motor.Op(
        
            db.accounts.update,
            {'account':res['account']},
            {'$addToSet':{''.join((resource, 
                                   '.ids')):res['id']},
             '$inc': {'resources.total':1,
                      ''.join((resource, '.total')):1}}
        )
    except Exception, e:
        callback(None, e)
        return
            
    callback(result, None)


@gen.engine
def get_unassigned_cdr(db, callback):
    '''
        Mango get unassigned cdr

        Periodic task that returns the unassigned CDR.
    '''
    try:
        result = []

        query = db.calls.find({'assigned':{'$exists':False}}).limit(1000)
        
        for c in (yield motor.Op(query.to_list)):
            calls.append(c)
            
    except Exception, e:
        callback(None, e)
    callback(calls, None)

@gen.engine
def process_assigned_false(db, callback):
    '''
        Mango process assigned false

        lol lol lol this is fucking nonsense

        Periodic task to process each false assigned
    '''

    result = []

    def _got_call(message, error):
        '''
            got call
        '''
        if message:
            channel = (message['channel'] if 'channel' in message else False)
            
            if channel:
                account = [a for a in _accounts 
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
            callback(None, error)
            return
        else:
            callback(result, None)
            return
    try:
        # Get mango account list
        _accounts = yield motor.Op(get_usernames, db)

        db.calls.find({
            'assigned':False
        }).limit(1000).each(_got_call)
    except Exception, e:
        callback(None, e)


@gen.engine
def process_asterisk_cdr(db, callback):
    '''
        Mango process asterisk cdr

        Periodic task that process each unassigned CDR.
        Periodic task to process new asterisk cdr entries.
    '''
    result = []

    def _got_call(message, error):
        '''
            got call
        '''
        if error:
            callback(None, error)
            return
            
        elif message:
            channel = (True if 'channel' in message else False)
            # get channel the value
            channel = (message['channel'] if channel else channel)
            
            if channel:
                account = [a for a in _accounts 
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
            #print 'hmmm'
            # Iteration complete
            callback(result, None)
            return
    
    try:
        # Get mango account list
        _accounts = yield motor.Op(get_usernames, db)

        db.calls.find({
            'assigned':{'$exists':False}
        }).limit(1000).each(_got_call)
    except Exception, e:
        callback(None, e)


@gen.engine
def assign_call(db, account, callid, callback):
    '''
        Mango assign call

        Update a call assigning it to an account.
    '''
    try:
        result = yield motor.Op(
            db.calls.update,
            {'_id':objectid.ObjectId(callid)}, 
            {'$set': {'assigned': True,
                      'accountcode':account}}
        )
        
    except Exception, e:
        callback(None, e)
        return
    
    callback(result, None)