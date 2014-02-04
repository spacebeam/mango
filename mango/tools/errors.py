#!/usr/bin/env python
'''
    Mango system errors.
'''


class Error(object):
    '''
        Mango custom error class
    '''
    
    def __init__(self, error):
        self.error = str(error)
        self.message = None
        self.data = None
    
    def model(self, model_name):
        '''
            Mango error model

            Dataset model
            
            model_name: Model name of the mango dataset to analize
        '''
        model_name = ''.join((model_name, ' resource'))
        self.message = self.error.split('-')[0].strip(' ').replace(
            'Model', model_name)
        self.data = ''.join(self.error.split('-')[1:]).replace(
            '  ', ' - ')
        
        return {
            'message': self.message,
            'errors': self.data
        }
        
    def duplicate(self, resource, field, value):
        '''
            Mango duplicate error

            Resource, field, value:
            Users username [\"ooo"\] already exists.
        '''
        self.message = ''.join((
            resource, ' ',
            field, ' ["', value, '"] already exists.'
        ))
        self.data = self.error
        
        return {
            'message': self.message,
            'errors': self.data
        }
    
    def json(self):
        '''
            Mango json error
        '''
        self.message = 'Invalid JSON Object'
        self.data = self.error
        
        return {
            'message': self.message,
            'errors': self.data
        }
    
    def missing(self, resource, name):
        '''
            Mango missing error
        '''
        self.message = 'Missing %s resource [\"%s\"].' % (resource, name)
        self.data = self.error
        
        return {
            'message': self.message,
            'errors': self.data
        }
    
    def invalid(self, resource, name):
        '''
            Mango invalid error
        '''
        self.message = 'Invalid %s resource [\"%s\"].' % (resource, name)
        self.data = self.error
        
        return {
            'message': self.message,
            'errors': self.data
        }