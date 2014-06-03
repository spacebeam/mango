# -*- coding: utf-8 -*-
'''
    Mango system logic.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import base64


def basic_authentication(handler_class):
    '''
        basic authentication
        --------------------

        HTTP Basic Authentication Decorator

        @basic_authentication
    '''

    def wrap_execute(handler_execute):
        '''
            Execute basic authentication

            Wrapper execute function
        '''

        def basic_auth(handler, kwargs):
            '''
                Basic AUTH implementation
            '''
            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Basic '):
                handler.set_status(403)
                handler.set_header('WWW-Authenticate', 'Basic '\
                                   'realm=mango')
                handler._transforms = []
                handler.finish()
                return False

            auth_decoded = base64.decodestring(auth_header[6:])
            handler.username, handler.password = auth_decoded.split(':', 2)

            print('A user just enter the dungeon! /api/ @basic_authentication')
            print('username', handler.username, 'password', handler.password)

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