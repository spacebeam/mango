# -*- coding: utf-8 -*-
'''
    Mango system errors.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


'''
    A supervisor is created to watch the servers and the servers 
    itself acts as monitors for the supervisor daemon.

    Most watchdog/supervisor type systems start two processes 
    that watch each other in addition to the target process(es).

    Monit and supervisord watch each other in addition to the system process(es).

    Inside our system overlords have monitor capabilities, of course overlords are build with Erlang.
'''


class Error(object):
    '''
        Mango custom error class
    '''
    
    def __init__(self, error):
        self.error = str(error)
        self.message = None
        self.hint = None
        self.data = None
        self.code = None

    def json(self):
        '''
            JSON error
        '''
        self.message = 'Invalid JSON Object'
        self.data = self.error

        return {
            'message': self.message,
            'errors': self.data
        }

    def msgpack(self):
        '''
            msgpack error
        '''
        self.message = 'Invalid Binary Object'
        self.data = self.error

        return {
            'message': self.message,
            'errors': self.data
        }

    def value(self):
        '''
            Value error
        '''
        self.message = 'Value Error'
        self.data = self.error

        return {
            'message': self.message,
            'errors': self.data
        }

    def model(self, model_name):
        '''
            Error model dataset
            
            model_name: Model name of the dataset
        '''
        model_name = ''.join((model_name, ' resource'))
        self.message = self.error.split('-')[0].strip(' ').replace(
            'Model', model_name)
        self.data = ''.join(
            self.error.split('-')[1:]).replace(
            '  ', ' - ')

        return {
            'message': self.message,
            'errors': self.data
        }

    def missing(self, resource, name):
        '''
            Missing error
        '''
        self.message = 'Missing %s resource [\"%s\"].' % (resource, name)
        self.data = self.error
        
        return {
            'message': self.message,
            'errors': self.data
        }

    def invalid(self, resource, name):
        '''
            Invalid error
        '''
        self.message = 'Invalid %s resource [\"%s\"].' % (resource, name)
        self.data = self.error

        return {
            'message': self.message,
            'errors': self.data
        }

    def duplicate(self, resource, field, value):
        '''
            Duplicate error
        '''
        self.message = ''.join((
            resource, ' ',
            field, ' ["', value, '"] invalid or already taken.'
        ))
        self.data = self.error

        return {
            'message': self.message,
            'errors': self.data
        }