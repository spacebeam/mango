# -*- coding: utf-8 -*-
'''
    Mango system tools.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import json
import motor

from datetime import datetime as dt

from tornado import gen
from mango.tools import errors
from mango.messages import reports


@gen.engine
def check_json(struct, callback):
    '''
        check json

        Check for malformed JSON Object
        < kind of iterator/function >
    '''
    try:
        struct = json.loads(struct)
    except Exception, e:
        api_error = errors.Error(e)
        error = api_error.json()
        callback(None, error)
        return

    callback(struct, None)

@gen.engine
def check_account_type(db, account, account_type, callback):
    '''
        check account type
    '''
    try:
        check_type = yield motor.Op(db.accounts.find_one,
                                    {'account': account,
                                     'type':account_type},
                                    {'type':1, '_id':0})
        if check_type:
            check_type = True
        else:
            check_type = False

    except Exception, e:
        callback(None, e)

    callback(check_type, None)

@gen.engine
def check_account_authorization(db, account, password, callback):
    '''
        Check account authorization
    '''
    try:
        account = yield motor.Op(db.accounts.find_one,
                                 {'account': account,
                                  'password': password})

    except Exception, e:
        callback(None, e)
        return

    callback(account, None)

@gen.engine
def check_aggregation_pipeline(struct, callback):
    '''
        Check aggregation pipeline

        Return mongodb aggregation report
    '''
    try:
        aggregation = reports.Aggregate(**struct).validate()
    except Exception, e:
        callback(None, e)
        return

    result = aggregation
    # TODO: test this method in action
    callback(result, None)

@gen.engine
def check_timestamp(start, stop, callback):
    '''
        Check timestamp
    '''
    try:
        start = (dt.fromtimestamp(float(start)) if start else None)
        stop = (dt.fromtimestamp(float(stop)) if stop else None)
    except Exception, e:
        callback(None, e)
        return

    callback({'start':start, 'stop':stop}, None)

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

    # results.get('results')
    results = results['results']

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

        @content_type_validation decorator
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
                handler.set_status(406)
                handler._transforms = []
                handler.finish({
                    'status': 406,
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