# -*- coding: utf-8 -*-
'''
    Mango accounts system logic.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import logging

import motor
import uuid

from tornado import gen

from mango.messages import accounts

from mango.tools import clean_structure, clean_results


class Accounts(object):
    '''
        Accounts main class
    '''

    @gen.coroutine
    def get_usernames(self):
        '''
            Get all the usernames
        '''
        accounts = yield self.db.accounts.find({}, {'account':1, '_id':0})
        
        raise gen.Return(accounts)

    @gen.coroutine
    def check_exist(self, account):
        '''
            Check if a given account exist
        '''
        exist = yield self.db.accounts.find_one(
                                {'account': account},
                                {'account':1, '_id':0})
        raise gen.Return(exist)

    @gen.coroutine
    def check_type(self, account, account_type):
        '''
            Check the type of a given account
        '''

        a_type = yield self.db.accounts.find_one(
                                        {'account': account,
                                         'account_type': account_type},
                                        {'type':1,'_id':0})
        
        raise gen.Return(a_type)

    @gen.coroutine
    def new_resource(self, struct):
        '''
            Create a new account resource
        '''
        try:
            res = accounts.AccountResource(struct)
            res.validate()
            res = res.to_primitive()
        except Exception, e:
            logging.exception(e)
            raise e

        resource = ''.join(('resources.', res['resource']))

        # add the account key with the current user

        if res.has_key('account') is False:
            res['account'] = self.get_current_user()
        
        result = yield self.db.accounts.update(
                        {'account':res['account']},
                        {
                         '$addToSet':{''.join((resource, '.contains')):res['uuid']},
                         '$inc': {'resources.total':1,
                         ''.join((resource, '.total')):1}
                        })

        raise gen.Return(result)

    @gen.coroutine
    def new_route(self, struct):
        '''
            New account billing route
        '''
        account = struct['account']
        try:
            route = accounts.Route(struct)
            route.validate()
            route = route.to_primitive()
        except Exception, e:
            logging.exception(e)
            raise e

        result = yield self.db.accounts.update(
                            {'account':account},
                            {'$addToSet':{'routes':route}})

        raise gen.Return(result)

    @gen.coroutine
    def get_route_list(self, account):
        '''
            Get account billing routes
        '''

        # Support for multiple routes missing

        result = yield self.db.accounts.find_one(
                            {'account': account},
                            {'routes':1, '_id':0})

        raise gen.Return(result)

    @gen.coroutine
    def get_orgs_list(self, account):
        '''
            Get account orgs
        '''
        result = yield self.db.accounts.find_one(
                            {'account': account},
                            {'orgs':1, '_id':0})

        raise gen.Return(result)


class MangoAccounts(Accounts):
    '''
        Mango accounts
    '''

    @gen.coroutine
    def get_accounts(self, account_type, page_num):
        '''
            Get the mango accounts
        '''
        # Query each and remove to_list better iteration stuff.

        page_size = self.settings['page_size']
        result = []

        query = self.db.accounts.find({'account_type':account_type})
        query = query.sort([('_id', -1)]).skip(int(page_num) * page_size).limit(page_size)

        for account in (yield query.to_list()):
            if 'user' in account_type:
                result.append(accounts.User(**account).validate())
            
            if 'org' in account_type:
                result.append(accounts.Org(**account).validate())

        gen.Return(result)

    @gen.coroutine
    def get_account(self, account, account_type):
        '''
            Get mango account
        '''
        result = yield self.db.accounts.find_one(
                                {'account':account,
                                 'account_type':account_type})
        if result:
            if 'user' in account_type:
                message = accounts.User(**result).validate()

            if 'org' in account_type:
                message = accounts.Org(**result).validate()
            
        raise gen.Return(message)

    @gen.coroutine
    def new_account(self, struct):
        '''
            New mango account
        '''
        account_type = struct['account_type']

        try:
            if 'user' in account_type:
                account = accounts.User(struct)

            if 'org' in account_type:
                account = accounts.Org(struct)

            account.validate()
            account = clean_structure(account)

        except Exception, e:
            logging.exception(e)
            raise e

        result = yield self.db.accounts.insert(account)

        raise gen.Return(account.get('uuid'))

    @gen.coroutine
    def remove_account(self, account):
        '''
            Remove mango account
        '''
        result = yield self.db.accounts.remove({'account':account})

        raise gen.Return(result)


class Orgs(MangoAccounts):
    '''
        Mango orgs accounts
    '''

    @gen.coroutine
    def get_bson_objectid(self, account):
        '''
            Get BSON _id
        '''
        result = yield self.db.accounts.find_one(
                    {'account':account}, {'_id':1})
        raise gen.Return(result)

    @gen.coroutine
    def get_uuid(self, account):
        '''
            Get uuid
        '''
        account_uuid = yield self.db.accounts.find_one(
                        {'account':account}, {'uuid':1})
        raise gen.Return(account_uuid)

    @gen.coroutine
    def new_member(self, org, user):
        '''
            New member
        '''
        update_user = self.db.accounts.update(
                            {'account':user},
                            {'$addToSet':{'orgs':org}})
        update_org = self.db.accounts.update(
                            {'account':org},
                            {'$addToSet':{'members':user}})

        result = yield [update_user, update_org]
        raise gen.Return(result)

    @gen.coroutine
    def get_member(self):
        '''
            Get member
        '''
        pass

    @gen.coroutine
    def check_member(self):
        '''
            Check member exist
        '''
        pass

    @gen.coroutine
    def get_members_list(self, org):
        '''
            Get members
        '''
        result = yield self.db.accounts.find_one(
                    {'account':org},
                    {'members':1, '_id':0})

        raise gen.Return(result)

    @gen.coroutine
    def remove_member(self, org, user):
        '''
            Remove member
        '''
        update_user = self.db.accounts.update(
                            {'account':user},
                            {'$pull':{'orgs':org}})
        update_org = self.db.accounts.update(
                            {'account': org},
                            {'$pull':{'members':user}})

        result = yield [update_user, update_org]
        raise gen.Return(result)

    @gen.coroutine
    def new_team(self, org, team):
        '''
            New team
        '''
        try:
            team = accounts.Team(**team).validate()
        except Exception, e:
            logging.exception(e)
            raise e

        result = yield self.db.accounts.update(
                        {'account':org},
                        {'$addToSet':{'teams':team}})
        raise gen.Return(result)

    @gen.coroutine
    def get_team(self):
        '''
            Get team
        '''
        pass

    @gen.coroutine
    def get_teams(self):
        '''
            Get teams
        '''
        pass

    @gen.coroutine
    def remove_team(self):
        '''
            Remove team
        '''
        pass