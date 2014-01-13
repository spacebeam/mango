# -*- coding: utf-8 -*-
'''
    Mango reports
'''
# This file is part of mango.
#
# Distributed under the terms of the last AGPL License. The full
# license is in the file LICENCE, distributed as part of this
# software.

__author__ = 'Jean Chassoul'


from tornado import gen

from mango.messages import reports

class Reports(object):
    '''
        Reports resources
    '''
    
    
    # TODO: research this stuff
    @gen.engine
    def new_aggregation_pipeline(self, struct, callback):
        '''
            Return mongodb aggregation report
        '''
        try:
            # change: reports.Aggregate(**struct) to (**struct).validate()
            aggregation = reports.Aggregate(**struct).validate()
            # aggregation.validate(True)
        except Exception, e:
            callback(None, e)
            return

        # change: aggregation.to_python() to result = aggregation or remove result
        # return just the aggregation object after validation()
        result = aggregation
        # TODO: test this method in action
        callback(result, None)
        