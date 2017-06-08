# -*- coding: utf-8 -*-
'''
    Mango accounts system logic functions.
'''
# 
# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import logging
import motor
import uuid
from tornado import gen
from mango.messages import accounts
from mango.tools import clean_structure, clean_results


class Accounts(object):
    '''
        Accounts main class

        Organisational programming class
    '''

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
    def get_account_list(self, account_type, status, page_num):
        '''
            Get the mango accounts
        '''
        account_list = []
        page_size = self.settings['page_size']

        query = {'account_type':account_type}
        if status != 'all':
            query['status'] = status
        query = self.db.accounts.find(query, {'_id':0})
        query = query.sort([('_id', -1)]).skip(int(page_num) * page_size).limit(page_size)
    
        try:
        
            while (yield query.fetch_next):
                account = query.next_object()
                account_list.append(account)
        except Exception, e:
            logging.exception(e)
            raise gen.Return(e)

        finally:
            raise gen.Return(account_list)

    @gen.coroutine
    def get_account(self, account, account_type):
        '''
            Get mango account
        '''
        message = None
        result = yield self.db.accounts.find_one(
                                {'account':account,
                                 'account_type':account_type},
                                 {'_id':0, 'password':0})
        if result:
            if 'user' in account_type:
                message = accounts.ModifyUser(result)
            elif 'org' in account_type:
                message = accounts.Org(result)
                
        try:
            if message:
                message.validate()
                message = clean_structure(message)
        except Exception, e:
            logging.exception(e)
            raise e
        finally:
            raise gen.Return(message)

    @gen.coroutine
    def get_account_uuid(self, account_uuid, account_type):
        '''
            Get mango account uuid
        '''
        message = None
        result = yield self.db.accounts.find_one(
                                {'uuid':account_uuid,
                                 'account_type':account_type},
                                 {'_id':0, 'password':0})
        if result:
            if 'user' in account_type:
                message = accounts.ModifyUser(result)
            elif 'org' in account_type:
                message = accounts.Org(result)
                
        try:
            if message:
                message.validate()
                message = clean_structure(message)
        except Exception, e:
            logging.exception(e)
            raise e
        finally:
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
            logging.error(e)
            raise e

        try:
            result = yield self.db.accounts.insert(account)
            message = account.get('uuid')
        except Exception, e:
            logging.error(e)
            message = str(e)

        raise gen.Return(message)

    @gen.coroutine
    def modify_account(self, account, account_uuid, struct):
        '''
            Modify task
        '''
        # note: yes is kind of crappy and stuff but we're doing it
        # the account unique query stuff instead of uuid.
        # uuid's are the answer, but...! there is no but, and this is nonsense.
        logging.warning('warning account_uuid not used on modify_account')
        try:
            schema = accounts.ModifyUser(struct)
            schema.validate()
            schema = clean_structure(schema)
        except Exception, e:
            logging.error(e)
            raise e

        try:
            result = yield self.db.accounts.update(
                {'account':account},
                # 'uuid':account_uuid},      read the note!
                {'$set':schema}
            )
            logging.warning(result)
        except Exception, e:
            logging.error(e)
            message = str(e)

        raise gen.Return(bool(result.get('n')))

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
        message = [bool(n.get('n')) for n in result]
        raise gen.Return(message)

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


        logging.warning(result)


        message = [n.get(n) for n in result]
        raise gen.Return(message)

    @gen.coroutine
    def new_team(self, org, team):
        '''
            New team
        '''
        # team validate and clean structure return team 
        # or log crash errors; variable assigned to team variable.
        try:
            team = accounts.Team(team) 
            team.validate()
            team = clean_structure(team)
        except Exception, e:
            logging.error(e)
            raise e
        try:
            message = yield self.db.accounts.update(
                {'account':org},
                {'$addToSet':{'teams':team}}
            )
        except Exception, e:
            logging.error(e)
            raise e

        raise gen.Return(bool(message.get('n')))

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