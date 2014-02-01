# -*- coding: utf-8 -*-
'''
    Mango accounts
'''
# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import datetime

import arrow
import motor
import uuid

import psycopg2
import momoko

from tornado import gen
from bson import objectid
from mango.messages import accounts

from mango.tools import clean_structure, clean_results


class Accounts(object):
    '''
        Accounts main class
    '''
    @gen.engine
    def get_usernames(self, callback):
        '''
            Get all the usernames
        '''
        accounts = []
        try:
            query = self.db.accounts.find({},{'account':1, '_id':0})
            
            for a in (yield motor.Op(query.to_list)):
                accounts.append(a)
        except Exception, e:
            callback(None, e)
        
        callback(accounts, None)

    @gen.engine
    def check_exist(self, account, callback):
        '''
            Check if a given account code exist
        '''
        try:
            exist = yield motor.Op(self.db.accounts.find_one,
                                   {'account': account}, 
                                   {'account':1, '_id':0})
            exist = (True if exist else False)

            
        except Exception, e:
            callback(None, e)
        
        callback(exist, None)
    
    @gen.engine
    def check_type(self, account, account_type, callback):
        '''
            Check the type of a given account
        '''
        try:
            check_type = yield motor.Op(self.db.accounts.find_one,
                                        {'account': account,
                                         'account_type': account_type},
                                        {'type':1,'_id':0})
            check_type = (True if check_type else False)
        except Exception, e:
            callback(None, e)
    
        callback(check_type, None)

    @gen.engine
    def new_resource(self, struct, callback):
        '''
            Create a new account resource
        '''
        try:
            res = accounts.AccountResource(struct)
            res.validate()
            res = res.to_primitive()
        except Exception, e:
            callback(None, e)
            return

        resource = ''.join(('resources.', res['resource']))

        # add the account key with the current user
        if res.has_key('account') is False:
            res['account'] = self.get_current_user()
        try:
            result = yield motor.Op(
                        self.db.accounts.update,
                        {'account':res['account']},
                        {
                         '$addToSet':{''.join((resource, '.contains')):res['uuid']},
                         '$inc': {'resources.total':1,
                         ''.join((resource, '.total')):1}
                        })

        except Exception, e:
            callback(None, e)
            return

        callback(result, None)

    @gen.engine
    def new_route(self, struct, callback):
        '''
            New account billing route
        '''
        account = struct['account']
        try:
            route = accounts.Route(struct)
            route.validate()
            route = route.to_primitive()
        except Exception, e:
            callback(None, e)
            return

        try:
            result = yield motor.Op(self.db.accounts.update,
                                    {'account':account},
                                    {'$addToSet':{'routes':route}})
        except Exception, e:
            callback(None, e)
            return

        callback(result, None)

    @gen.engine
    def get_routes(self, account, callback):
        '''
            Get account billing routes
        '''

        # Support for multiple routes missing !!!

        # TBD by a funhead.

        try:
            result = yield motor.Op(self.db.accounts.find_one,
                                    {'account': account},
                                    {'routes':1, '_id':0})   
        except Exception, e:
            callback(None, e)
            return

        print(result, 'get in out with the stuff')
        callback(result, None)

    @gen.engine
    def get_orgs(self, account, callback):
        '''
            Get account orgs
        '''

        try:
            result = yield motor.Op(self.db.accounts.find_one,
                                    {'account': account},
                                    {'orgs':1, '_id':0})
        except Exception, e:
            callback(None, e)
            return
        
        callback(result, None)

class MangoAccounts(Accounts):
    '''
        Mango accounts
    '''
    
    @gen.engine
    def get_accounts(self, account_type, page_num, callback):
        '''
        
            Get the mango accounts
        
        '''
        # Research query each and remove to_list better iteration stuff 
        account_type = account_type
        page_num = int(page_num)
        page_size = self.settings['page_size']
        result = []
        try:
            query = self.db.accounts.find({'account_type':account_type}).sort(
                [('_id', -1)]).skip(page_num * page_size).limit(page_size)
            
            for account in (yield motor.Op(query.to_list)):
                if 'user' in account_type:
                    result.append(accounts.User(**account).validate())
                elif 'org' in account_type:
                    result.append(accounts.Org(**account).validate())
                else:
                    callback(None, account_type)
        except Exception, e:
            callback(None, e) 
        
        callback(result, None)
    
    @gen.engine
    def get_account(self, account, account_type, callback):
        '''
        
            Get a mango account
        
        '''
        account = account
        account_type = account_type
        try:
            account = yield motor.Op(self.db.accounts.find_one,
                                     {'account':account,
                                      'account_type':account_type})
            if account:
                if 'user' in account_type:
                    account = accounts.User(**account).validate()
                elif 'org' in account_type:
                    account = accounts.Org(**account).validate()
                else:
                    callback(None, account_type)
        except Exception, e:
            callback(None, e)
        
        callback(account, None)


    @gen.engine
    def new_account(self, struct, callback):
        '''
            New mango account
        '''
        account_type = struct['account_type']
        
        try:
            if 'user' in account_type:
                account = accounts.User(struct)
            elif 'org' in account_type:
                account = accounts.Org(struct)
            else:
                callback(None, account_type)
                return

            account.validate()
            account = clean_structure(account)

        except Exception, e:
            callback(None, e)
            return
        
        try:
            result = yield motor.Op(self.db.accounts.insert, account)
        except Exception, e:
            callback(None, e)
            return

        callback(account['uuid'], None)


    @gen.engine
    def new_sip_account(self, struct, callback):
        '''
            New sip account
        '''
        try:
            query = '''
                insert into sip (
                    name,
                    defaultuser,
                    fromuser,
                    fromdomain,
                    host,
                    sippasswd,
                    allow,
                    context,
                    avpf,
                    encryption
                ) values (
                    '%s',
                    '%s',
                    '%s',
                    'sip.ph3nix.com',
                    'dynamic',
                    '%s',
                    'g729,gsm,alaw,ulaw',
                    'fun-accounts',
                    'no',
                    'no'
                );
            ''' % (struct['account'],
                   struct['account'],
                   struct['account'],
                   struct['password'])

            cursor = yield momoko.Op(self.sql.execute, query)

        except (psycopg2.Warning, psycopg2.Error) as error:
            callback(None, str(error))
            return
        else:
            result = True

        callback(result, None)


    @gen.engine
    def remove_account(self, account, callback):
        '''
            Remove mango account
        '''
        account = account
        try:
            result = yield motor.Op(self.db.accounts.remove,
                                    {'account':account})
        except Exception, e:
            callback(None, e)
            return
        
        callback(result, None)


class Orgs(MangoAccounts):
    '''
        Mango orgs accounts
    '''
    
    @gen.engine
    def get_id(self, account, callback):
        '''
            Get id
        '''
        try:
            account_id = yield motor.Op(self.db.accounts.find_one,
                                        {'account':account}, {'_id':1})
        except Exception, e:
            callback(None, e)
        
        callback(account_id, None)

    @gen.engine
    def get_uuid(self, account, callback):
        '''
            Get uuid
        '''
        try:
            account_uuid = yield motor.Op(self.db.accounts.find_one,
                                        {'account':account}, {'uuid':1})
        except Exception, e:
            callback(None, e)
        
        callback(account_uuid, None)
    
    @gen.engine
    def new_member(self, org, user, callback):
        '''
            New member
        '''
        try:
            result = yield [
                motor.Op(self.db.accounts.update, 
                         {'account':user}, 
                         {'$addToSet':{'orgs':org}}),
                motor.Op(self.db.accounts.update,
                         {'account':org},
                         {'$addToSet':{'members':user}})
            ]
        except Exception, e:
            callback(None, e)
        
        callback(result, None)

    @gen.engine
    # get member
    # check_member
    def check_member(self, callback):
        '''
            Check member exist
        '''
        pass
    
    @gen.engine
    def get_members(self, org, callback):
        '''
            Get members
        '''
        try:
            result = yield motor.Op(self.db.accounts.find_one,
                                    {'account':org}, {'members':1, '_id':0})
        except Exception, e:
            callback(None, e)

        callback(result, None)
    
    @gen.engine
    def remove_member(self, org, user, callback):
        '''
            Remove member
        '''

        # TODO: remove/clean this
        result = None

        try:
            result = yield [
                motor.Op(self.db.accounts.update, 
                         {'account':user}, 
                         {'$pull':{'orgs': org}}),
                motor.Op(self.db.accounts.update,
                         {'account': org},
                         {'$pull':{'members': user}})
            ]
        except Exception, e:
            callback(None, e)
        
        #result = (result if result else False)
        print('remove_member', result)
        
        callback(result, None)
    
    
    @gen.engine
    def new_team(self, org, team, callback):
        '''
            New team
        '''
        try:
            team = accounts.Team(**team).validate()
        except Exception, e:
            callback(None, e)
        
        result = yield motor.Op(self.db.accounts.update,
                                {'account':org},
                                {'$addToSet': {'teams':team}})
        
        callback(result, None)
    
    @gen.engine
    def get_team(self, callback):
        '''
            Get team
        '''
        pass
    
    @gen.engine
    def get_teams(self, callback):
        '''
            Get teams
        '''
        pass
    
    @gen.engine
    def remove_team(self, callback):
        '''
            Remove team
        '''
        pass