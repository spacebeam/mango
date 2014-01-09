# -*- coding: utf-8 -*-
'''
    Mango billings handlers
'''
# This file is part of mango.
#
# Distributed under the terms of the last AGPL License. The full
# license is in the file LICENCE, distributed as part of this
# software.

__author__ = 'Jean Chassoul'


import motor

import pandas as pd

from tornado import gen
from tornado import web

from mango.system import accounts
from mango.system import billings
from mango.system import records

from mango.handlers import BaseHandler
from mango.tools import content_type_validation
from mango.tools import errors
from mango.tools import check_json


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
    
    @web.authenticated
    @web.asynchronous
    @gen.engine
    def get(self, start=None, stop=None):
        '''
            Mango get record billing handler

            GET Method Response
        '''
        account = self.get_current_user()
        routes = yield motor.Op(self.get_routes, account)
        elapse = 'hours'
        billing = 0
        
        orgs = yield motor.Op(self.get_orgs, account)
        mango_accounts = (orgs['orgs'] if orgs else False)
        if mango_accounts:
            mango_accounts.append(account)

        # TODO: fix billing for multiple routes

        if routes:
            single = (routes['routes'][0] if routes['routes'] else None)
            if single:
                if mango_accounts:
                    result = yield motor.Op(self.get_cost_summary, mango_accounts, single, elapse)
                else:
                    result = yield motor.Op(self.get_cost_summary, account, single, elapse)

            # pandas data frame
            frame = (pd.DataFrame(result) if result else pd.DataFrame([{'billsecs': 0}]))
            
            # calculate the minutes
            frame['minutes'] = frame['billsecs'] / 60

            # calculate the cost and add the result to the dataframe
            frame['billing'] = frame['minutes'] * single_route['cost']
            
            # set the billing
            billing = frame['billing'].sum()
        
        self.finish({
            'billing': '%.2f' % billing
        })
        