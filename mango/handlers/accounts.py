# -*- coding: utf-8 -*-
'''
    Mango HTTP accounts handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import motor

import logging

# import numpy as np
# import pandas as pd

from tornado import gen
from tornado import web

from mango.system import accounts
from mango.system import records

from mango.tools import content_type_validation
from mango.tools import check_json

from mango.tools import errors

from mango.handlers import BaseHandler


@content_type_validation
class UsersHandler(accounts.MangoAccounts, BaseHandler):
    '''
        User accounts HTTP request handlers
    '''

    @web.authenticated
    @gen.coroutine
    def get(self, account=None, page_num=0):
        '''
            Get user accounts
        '''
        account_type = 'user'
        if not account:
            users = yield self.get_account_list(account_type, page_num)
            self.finish({'users':users})
        else:
            account = account.rstrip('/')
            result = yield self.get_account(account, account_type)
            
            if not result:
                self.set_status(400)
                self.finish({'missing':account})
                return
            else:
                self.finish(result)
                return
                
    @gen.coroutine
    def post(self):
        '''
            Create user account
        '''
        struct = yield check_json(self.request.body)
        
        format_pass = (True if struct else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return

        struct['account_type'] = 'user'

        #logging.info(struct)

        result = yield self.new_account(struct)

        if 'error' in result:
            model = 'User'
            reason = {'duplicates': [(model, 'account'), (model, 'email')]}

            message = yield self.let_it_crash(struct, model, result, reason)

            logging.warning(message)

            self.set_status(400)
            self.finish(message)
            return


        # -- handle SIP account creation out-of-band

        # postgresql insert sip account
        if result:
            sip_account = yield self.new_sip_account(struct)


        self.set_status(201)
        self.finish({'id':result})

    @web.authenticated
    @gen.coroutine
    def delete(self, account):
        '''
            Delete a user account
        '''
        account = account.rstrip('/')
        result = yield self.remove_account(account)

        # why we're using result['n']?

        import pprint
        pprint(result)
        print('''delete check result['n'] on UsersHandler''')

        if not result['n']:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('user', account)
            self.finish(error)
            return

        self.set_status(204)
        self.finish()


@content_type_validation
class OrgsHandler(accounts.Orgs, BaseHandler):
    '''
        Organization account resource handlers
    '''

    @web.authenticated
    @gen.coroutine
    def get(self, account=None, page_num=0):
        '''
            Mango organization accounts get handler
            
            Get organization accounts
        '''
        account_type = 'org'
        if not account:
            orgs = yield self.get_account_list(account_type, page_num) 
            self.finish({'orgs':orgs})
        else:
            account = account.rstrip('/')

            result = yield self.get_account(account, account_type)
            
            if result:
                self.finish(result)
                return
            else:
                self.set_status(400)
                self.finish({'missing':account})
                return

    @gen.coroutine
    def post(self):
        '''
            Create organization accounts
        '''
        current_user = self.get_current_user()
        
        if not current_user:
            current_user = 'capnkooc'
        
        struct = yield check_json(self.request.body)
        struct['account_type'] = 'org'

        org = struct['account']
        
        format_pass = (True if struct else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return

        org_id = yield self.new_account(struct)
                
        team = {
            'name': 'owners',
            'permission': 'super',
            'members': [current_user]
        }

        print(org, team)

        check_member = yield self.new_member(org, current_user)
        check_team = yield self.new_team(org, team)


        print('org_id', org_id)
        print('member', check_member)
        print('team', check_team)

        if not org_id:
            print('some errors')
            self.set_status(400)
            self.finish({'errors':struct})
            return

        self.set_status(201)
        self.finish({'id':org_id})

    @web.authenticated
    @gen.coroutine
    def delete(self, account):
        '''
            Mango organization accounts delete handler
        
            Delete a organization account
        '''
        org = account.rstrip('/')
        
        # for each member in members remove member.
        members = yield self.get_members(org)
        members = (members['members'] if members['members'] else False)
        
        # clean this hack
        
        for user in members:
            rmx = yield self.remove_member(org, user)
            
        # check_member = yield self.remove_member(org_id, current_user)
        
        result = yield self.remove_account(org)

        # again with the result['n'] stuff... what is this shit?
        print('check for n stuff', result)
        
        if not result['n']:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('org', org)
            self.finish(error)
            return

        self.set_status(204)
        self.finish()


@content_type_validation
class TeamsHandler(accounts.Orgs, BaseHandler):
    '''
        Teams resource handlers
    '''
    pass


@content_type_validation
class MembersHandler(accounts.Orgs, BaseHandler):
    '''
        Members resource handlers
    '''
    pass


@content_type_validation
class RecordsHandler(accounts.Accounts, records.Records, BaseHandler):
    '''
        Records resource handlers
    '''

    @web.authenticated
    @gen.coroutine
    def get(self, account, page_num=0):
        '''
            Get records handler
        '''
        # check_type account with organizations
        #account_type = yield self.check_type(account, 'user')
        
        orgs = yield self.get_orgs_list(account)
        
        print(orgs, 'organizations')
        
        #if not account_type:
        #    system_error = errors.Error('invalid')
        #    self.set_status(400)
        #    error = system_error.invalid('user', account)
        #    self.finish(error)
        #    return

        print(account, page_num)

        result = yield self.get_record_list( 
                            account=account, 
                            page_num=page_num,
                            lapse=None,
                            start=None,
                            end=None)

        self.finish(result)
        
    @web.authenticated
    @gen.coroutine
    def post(self, account):
        '''
            Post records handler
        '''
        struct = yield check_json(self.request.body)
        
        format_pass = (True if struct else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        
        if account == self.get_current_user():
            struct['account'] = account
        
        # check if ORGs follows same pattern.
        
        else:
            self.set_status(404)
            self.finish({'WARNING':'Pre-Access patterns research'})
            return
        
        record = yield self.new_detail_record(struct)

        if not record:
            model = 'Records'
            error = {'record':False}
            reason = {'duplicates':[('Record', 'uniqueid'), (model, 'uuid')]}

            message = yield self.let_it_crash(struct, model, error, reason)

            self.set_status(400)
            self.finish(message)
            return

        # -- handle this out-of-band.

        struct = {'account':account,
                  'resource': 'records',
                  'id': record}

        update = yield self.new_resource(struct)

        if not update:
            print('WARNING: error on new_resource record update.')

        # logging update resource info
        print(update)

        # id -> uuid
        # id same as uuid.

        self.set_status(201)
        self.finish({'id':record})
    
    @web.authenticated
    @gen.coroutine
    def delete(self, account, record=None, page_num=0):
        '''
            Delete
        '''
        pass
    
    @web.authenticated
    @gen.coroutine
    def put(self, account, record=None, page_num=0):
        '''
            Put
        '''
        pass
    
    @web.authenticated
    @gen.coroutine
    def patch(self, account, record=None, page_num=0):
        '''
            Patch
        '''
        pass


@content_type_validation
class RoutesHandler(accounts.Accounts, BaseHandler):
    '''
        Routes resource handlers
    '''
    
    @web.authenticated
    @gen.coroutine
    def get(self, account):

        # get account the record billing routes from the database
        
        routes = yield self.get_route_list(account)
        self.finish(routes)
        
        
    #@web.authenticated
    @gen.coroutine
    def post(self, account):
        '''
            Create new record billing route
        '''
        
        struct = yield check_json(self.request.body)
        
        # where is the error msg?

        if not struct:
            self.set_status(400)
            self.finish(error)
            return
        
        struct['account'] = account
        
        print(struct)
        
        result = yield self.new_route(struct)

        self.finish()