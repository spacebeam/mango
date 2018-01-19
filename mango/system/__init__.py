# -*- coding: utf-8 -*-
'''
    Mango system logic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import time
import random
import logging
import base64


def basic_authentication(handler_class):
    '''
        @basic_authentication

        HTTP Basic Authentication Decorator
    '''

    def wrap_execute(handler_execute):
        '''
            Wrap Execute basic authentication function
        '''

        def basic_auth(handler, kwargs):
            '''
                Basic AUTH implementation
            '''
            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Basic '):
                handler.set_status(403)
                handler.set_header('WWW-Authenticate', 'Basic '\
                                   'realm=mango') # get realm for somewhere else.
                handler._transforms = []
                handler.finish()
                return False
            logging.warning(auth_header[6:])
            auth_decoded = base64.b64encode(auth_header[6:])
            #auth_decoded = base64.decodestring(auth_header[6:])
            #logging.warning(auth_decoded)
            #handler.username, handler.password = auth_decoded.split(':', 2)
            logging.info('%s enter the dungeon! @basic_auth' % handler.username)
            return True

        def _execute(self, transforms, *args, **kwargs):
            '''
                Execute the wrapped function
            '''
            if not basic_auth(self, kwargs):
                return False
            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)

    return handler_class
