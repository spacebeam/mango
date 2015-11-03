# -*- coding: utf-8 -*-
'''
    Mango addresses system logic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import logging

import arrow
import motor

import uuid

# import numpy as np
import pandas as pd

from tornado import gen

from mango.messages import addresses
from mango.messages import reports

from mango.tools import clean_structure
from mango.tools import clean_results
from mango.tools import check_times


class Addresses(object):
    '''
        Addresses resources
    '''

    @gen.coroutine
    def get_address(self, account, address_uuid):
        '''
            Get a detail address
        '''
        if not account:
            address = yield self.db.addresses.find_one({'uuid':address_uuid},{'_id':0})
        else:

            # change accountcode to account, because the accountcode is a uuid
            # and we're expecting an account name.

            address = yield self.db.addresses.find_one({'uuid':address_uuid,'account':account},{'_id':0})
        try:
            if address:
                address = addresses.Address(address)
                address.validate()
        except Exception, e:
            # catch some daemon here!
            # so we send the exception down the drain, down the the rat hole, the rabbit hole, etc
            # but, it does not disapeer, if everything is set, the monitor,supervisor,overlord will know.
            logging.exception(e) 
            raise e
        # we use this last finally to raise gen.Return only because of python version 2.7 stuff
        finally:
            raise gen.Return(address)

    @gen.coroutine
    def get_address_list(self, account, start, end, lapse, status, page_num):
        '''
            Get detail addresses 
        '''
        page_num = int(page_num)
        page_size = self.settings['page_size']
        address_list = []
        message = None
        query = {'public':False}

        if status != 'all':
            query['status'] = status
        
        if not account:
            query = self.db.addresses.find(query,
                                       {'_id':0, 'comments':0})
        elif type(account) is list:
            accounts = [{'accountcode':a, 'assigned': True} for a in account]
            query = self.db.addresses.find({'$or':accounts},
                                       {'_id':0, 'comments':0})
        else:
            query = self.db.addresses.find({'accountcode':account,
                                        'assigned':True},
                                       {'_id':0, 'comments':0})
        
        query = query.sort([('uuid', -1)]).skip(page_num * page_size).limit(page_size)
        
        try:
            
            while (yield query.fetch_next):
                result = query.next_object()
                address_list.append(addresses.Address(result))

        except Exception, e:
            logging.exception(e)
            raise e

        try:
            struct = {'results': address_list}

            # reports BaseGoal? da faq??
            
            message = reports.BaseGoal(struct)
            message.validate()
            message = clean_results(message)

        except Exception, e:
            logging.exception(e)
            raise e
        finally:
            raise gen.Return(message)
    
    @gen.coroutine
    def get_unassigned_addresses(self, start, end, lapse, page_num):
        '''
            Get unassigned addresses
        '''
        page_num = int(page_num)
        page_size = self.settings['page_size']
        result = []
        
        # or $exist = false ?

        query = self.db.addresses.find({'assigned':False})
        query = query.sort([('uuid', -1)]).skip(page_num * page_size).limit(page_size)
        
        try:
            for address in (yield query.to_list()):
                result.append(addresses.Address(address))
            
            struct = {'results':result}

            results = reports.BaseResult(struct)
            results.validate()
        except Exception, e:
            logging.exception(e)
            raise e

        results = clean_results(results)        
        raise gen.Return(results)


    @gen.coroutine
    def new_address(self, struct):
        '''
            Create a new address entry
        '''
        try:
            address = address.Address(struct)
            address.validate()
        except Exception, e:
            logging.exception(e)
            raise e

        address = clean_structure(address)

        result = yield self.db.addresses.insert(address)

        raise gen.Return(address.get('uuid'))

    @gen.coroutine
    def set_assigned_flag(self, account, address_uuid):
        '''
            Set the address assigned flag
        '''
        logging.info('set_assigned_flag account: %s, address: %s' % (account, address_uuid))

        result = yield self.db.addresses.update(
                                {'uuid':address_uuid, 
                                 'accountcode':account}, 
                                {'$set': {'assigned': True}})
        
        raise gen.Return(result)

    @gen.coroutine
    def remove_address(self, address_uuid):
        '''
            Remove a address entry
        '''
        result = yield self.db.addresses.remove({'uuid':address_uuid})
        raise gen.Return(result)

    @gen.coroutine
    def modify_address(self, account, address_uuid, struct):
        '''
            Modify address
        '''
        try:
            logging.info(struct)
            address = addresses.ModifyAddress(struct)
            address.validate()
            address = clean_structure(address)
        except Exception, e:
            logging.error(e)
            raise e

        try:
            result = yield self.db.addresses.update(
                {'account':account,
                 'uuid':address_uuid},
                {'$set':address}
            )
            logging.info(result)            
        except Exception, e:
            logging.error(e)
            message = str(e)

        raise gen.Return(bool(result.get('n')))

    @gen.coroutine
    def replace_address(self, struct):
        '''
            Replace a existent address entry
        '''
        # put implementation
        pass

    @gen.coroutine
    def resource_options(self):
        '''
            Return resource options
        '''
        # options implementation
        pass