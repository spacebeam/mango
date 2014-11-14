# -*- coding: utf-8 -*-
'''
    Mango reports system logic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


from tornado import gen

from mango.messages import reports


'''
    This is nonsense.
'''


class Reports(object):
    '''
        Reports resources
    '''
    
    # it's all about pipes.
    @gen.coroutine
    def new_aggregation_pipeline(self, struct):
        '''
            Return mongodb aggregation result
        '''
        try:
            aggregation = reports.Aggregate(**struct).validate()
        except Exception, e:
            logging.exception(e)
            raise e

        # change: aggregation.to_python() to result = aggregation or remove result
        # return just the aggregation object after validation()
        result = aggregation
        
        # fix or remove this stuff out.

        raise gen.Return(result)