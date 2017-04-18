# -*- coding: utf-8 -*-
'''
    Mango tools system logic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import time
import arrow
import ujson as json
import motor
import logging
from tornado import gen
from mango import errors
from mango.messages import accounts


def get_average(total, marks):
    '''
        Get average from signals
    '''
    return float(total) / len(marks)

def get_percentage(shit, stuff):
    '''
        Get percentage of shit and stuff.

    '''
    return "{:.0%}".format(shit/stuff)

@gen.coroutine
def check_json(struct):
    '''
        Check for malformed JSON
    '''
    try:
        struct = json.loads(struct)
    except Exception, e:
        api_error = errors.Error(e)
        error = api_error.json()

        logging.exception(e)
        raise gen.Return(error)

        return

    raise gen.Return(struct)

@gen.coroutine
def check_account_type(db, account, account_type):
    '''
        check account type
    '''
    try:
        check_type = yield db.accounts.find_one({'account': account,
                                                 'type':account_type},
                                                {'type':1, '_id':0})
    except Exception, e:
        logging.exception(e)
        raise e

        return

    raise gen.Return(check_type)

@gen.coroutine
def check_account_authorization(db, account, password):
    '''
        Check account authorization
    '''
    try:
        message = yield db.accounts.find_one({'account': account,
                                              'password': password})

    except Exception, e:
        logging.exception(e)
        raise e

        return

    raise gen.Return(message)
    
@gen.coroutine
def check_times(start, end):
    '''
        Check times
    '''
    try:
        start = (arrow.get(start) if start else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))

        start = start.timestamp
        end = end.timestamp

    except Exception, e:
        logging.exception(e)
        raise e

        return

    message = {'start':start, 'end':end}
    
    raise gen.Return(message)

@gen.coroutine
def check_times_get_timestamp(start, end):
    '''
        Check times
    '''
    try:
        start = (arrow.get(start) if start else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))
    except Exception, e:
        logging.exception(e)
        raise e

        return

    message = {'start':start.timestamp, 'end':end.timestamp}
    
    raise gen.Return(message)

@gen.coroutine
def check_times_get_datetime(start, end):
    '''
        Check times
    '''
    try:
        start = (arrow.get(start) if start else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))
    except Exception, e:
        logging.exception(e)
        raise e

        return

    message = {'start':start.naive, 'end':end.naive}
    
    raise gen.Return(message)

@gen.coroutine
def new_resource(db, struct, collection=None, scheme=None):
    '''
        New resource function
    '''

    # and now for something completely different
    # we're moving the complete new_structure stuff
    # to the treehouse structure.

    import uuid as _uuid
    from schematics import models as _models
    from schematics import types as _types

    # Trying to find analogies with erlang records
    # We need more experience on OTP.
    class MangoResource(_models.Model):
        '''
            Mango resource
        '''
        uuid = _types.UUIDType(default=_uuid.uuid4)
        account = _types.StringType(required=False)
        resource  = _types.StringType(required=True)


    # Calling getattr(x, "foo") is just another way to write x.foo
    collection = getattr(db, collection)  

    try:
        message = MangoResource(struct)
        message.validate()
        message = message.to_primitive()
    except Exception, e:
        logging.exception(e)
        raise e
        return

    resource = 'resources.{0}'.format(message.get('resource'))

    try:
        message = yield collection.update(
            {
                #'uuid': message.get(scheme),           # tha fucks ?
                'account': message.get('account')
            },
            {
                '$addToSet': {
                    '{0}.contains'.format(resource): message.get('uuid')
                },
                    
                '$inc': {
                    'resources.total': 1,
                    '{0}.total'.format(resource): 1
                }
            }
        )
    except Exception, e:
        logging.exception(e)
        raise e
        return

    raise gen.Return(message)

def clean_message(struct):
    '''
        clean message structure
    '''
    struct = struct.to_native()

    struct = {
        key: struct[key] 
            for key in struct
                if struct[key] is not None
    }

    return struct

def clean_structure(struct):
    '''
        clean structure
    '''
    struct = struct.to_primitive()

    struct = {
        key: struct[key] 
            for key in struct
                if struct[key] is not None
    }

    return struct

def clean_results(results):
    '''
        clean results
    '''
    results = results.to_primitive()
    results = results.get('results')

    results = [
        {
            key: dic[key]
                for key in dic
                    if dic[key] is not None 
        } for dic in results 
    ]

    return {'results': results}