# -*- coding: utf-8 -*-
'''
    Mango system logic function tools.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import time
import arrow
import json
import motor

import logging

from tornado import gen
from mango.tools import errors

from mango.messages import accounts
from mango.messages import reports


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
def check_aggregation_pipeline(struct):
    '''
        Check aggregation pipeline

        Return mongodb aggregation report
    '''
    try:
        aggregation = reports.Aggregate(**struct).validate()
    except Exception, e:
        logging.exception(e)
        raise e

        return

    message = aggregation

    # TODO: test this in action
    
    raise gen.Return(message)
    
@gen.coroutine
def check_times(start, end):
    '''
        Check times
    '''
    try:
        start = (arrow.get(start) if start else arrow.utcnow())
        end = (arrow.get(end) if end else start.replace(days=+1))

        start = start.timestamp
        end = end.timestamp

    except Exception, e:
        logging.exception(e)
        raise e

        return

    message = {'start':start, 'end':end}
    
    raise gen.Return(message)

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

def content_type_validation(handler_class):
    '''
        Content type validation
    
        @decorator
    '''

    def wrap_execute(handler_execute):
        '''
            Content-Type checker

            Wrapper execute function
        '''
        def ctype_checker(handler, kwargs):
            '''
                Content-Type checker implementation
            '''
            content_type = handler.request.headers.get("Content-Type", "")
            if content_type is None or not content_type.startswith('application/json'):
                handler.set_status(415)
                handler._transforms = []
                handler.finish({
                    'status': 415,
                    'reason': 'Unsupported Media Type',
                    'message': 'Must ACCEPT application/json: '\
                    '[\"%s\"]' % content_type 
                })
                return False
            return True

        def _execute(self, transforms, *args, **kwargs):
            '''
                Execute the wrapped function
            '''
            if not ctype_checker(self, kwargs):
                return False
            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class

@gen.coroutine
def new_resource(db, struct):
    '''
        New resource
    '''
    import uuid as _uuid
    from schematics import models as _models
    from schematics import types as _types

    class AccountResource(_models.Model):
        '''
            Account resource
        '''
        account = _types.StringType(required=False)
        uuid = _types.UUIDType(default=_uuid.uuid4)
        resource  = _types.StringType(required=True)

    try:
        message = AccountResource(struct)
        message.validate()
        message = message.to_primitive()
    except Exception, e:
        logging.exception(e)
        raise e

        return

    resource = ''.join(('resources.', message.get('resource')))

    logging.info(resource)
    logging.info({''.join((resource, '.contains')): message.get('uuid')})
    logging.info(''.join((resource, '.total')))
    logging.info({
                'uuid': message.get('uuid'),
                'account': message.get('account')
            })

    try:
        message = yield db.accounts.update(
            {
                'uuid': message.get('uuid'),
                'account': message.get('account')
            },
            {
                '$addToSet': {
                    ''.join((resource, '.contains')): message.get('uuid')
                },
                    
                '$inc': {
                    'resources.total': 1,
                    ''.join((resource, '.total')): 1
                }
            }
        )
    except Exception, e:
        logging.exception(e)
        raise e

        return

    raise gen.Return(message)

@gen.coroutine
def resource_exists(db, struct):
    '''
        resource_exists

        exist, exists, existed
    '''

@gen.coroutine
def last_modified(db, struct):
    '''
        last_modified

        exist, exists, existed
    '''

@gen.coroutine
def moved_permanently(db, struct):
    '''
        moved_permanently

        exist, exists, existed
    '''

@gen.coroutine
def moved_temporarily(db, struct):
    '''
        moved_temporarily

        exist, exists, existed
    '''

@gen.coroutine
def previously_existed(db, struct):
    '''
        previosly_existed

        exist, exists, existed
    '''

@gen.coroutine
def resource_exists(db, struct):
    '''
        resource_exists

        exist, exists, existed
    '''

@gen.coroutine
def forbidden_resource(db, struct):
    '''
        forbidden_resource

        exist, exists, existed
    '''

@gen.coroutine
def delete_resource(db, struct):
    '''
        delete_resource

        exist, exists, existed
    '''

@gen.coroutine
def delete_completed(db, struct):
    '''
        delete_resource
    '''