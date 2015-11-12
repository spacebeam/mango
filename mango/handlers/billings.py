# -*- coding: utf-8 -*-
'''
    Mango HTTP billings handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import time
import motor

# import numpy as np
# import pandas as pd

import logging

from tornado import gen
from tornado import web

from mango.system import accounts
from mango.system import billings
from mango.system import records

from mango.tools import content_type_validation
from mango.tools import check_json
from mango import errors

from mango.handlers import BaseHandler


@content_type_validation
class BillingsHandler(BaseHandler):
    '''
        Mango billings handler
    '''
    pass


@content_type_validation
class RecordsHandler(billings.Billings, accounts.Accounts, BaseHandler):
    '''
        Mango records billings handler 

        Billings handlers for records resources
    '''
    
    ##@web.authenticated
    @gen.coroutine
    def get(self, start=None, end=None):
        '''
            Mango get record billing handler

            GET Method Response
        '''
        account = self.get_current_username()
        routes = yield self.get_route_list(account)
        lapse = 'hours'
        
        billing = 0
        
        orgs = yield self.get_orgs_list(account)
        account_list = (orgs['orgs'] if orgs else False)
        if account_list:
            account_list.append(account)

        # WARNING: Missing billing for multiple route list.

        if routes:
            single = (routes['routes'][0] if routes['routes'] else None)
            if single:
                if account_list:
                    result = yield self.get_cost_summary(account_list, single, elapse)
                else:
                    result = yield self.get_cost_summary(account, single, elapse)

            # pandas data frame
            frame = (pd.DataFrame(result) if result else pd.DataFrame([{'seconds': 0}]))
            
            # calculate the minutes
            frame['minutes'] = frame['seconds'] / 60

            # calculate the cost and add the result to the dataframe
            frame['billing'] = frame['minutes'] * single_route['cost']
            
            # set the billing
            billing = frame['billing'].sum()
        
        self.finish({
            'billing': '%.2f' % billing
        })

@content_type_validation
class SeatsHandler(billings.Billings, accounts.Accounts, BaseHandler):
    '''
        Seats Billing Handler
    '''
    pass