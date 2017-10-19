# -*- coding: utf-8 -*-
'''
    HTTP accounts handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import uuid
import logging
import ujson as json
from tornado import gen
from tornado import web
from mango.messages import accounts as models
from mango.system import accounts, groups, orgs
from tornado import httpclient
from mango.tools import errors, str2bool, check_json
from mango.handlers import BaseHandler


class UsersHandler(accounts.Account, BaseHandler):
    '''
        HTTP request handlers
    '''

    @gen.coroutine
    def head(self, account=None, account_uuid=None, page_num=0):
        '''
            Head accounts
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_username_cookie()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # not unique
        unique = query_args.get('unique', False)
        # rage against the finite state machine
        status = 'all'
        # are we done yet?
        done = False
        # some random that crash this shit
        message = {'crashing': True}
        # unique flag activated
        if unique:
            unique_stuff = {key:query_args[key][0] for key in query_args}
            account_list = yield self.get_unique_queries(unique_stuff)
            unique_list = yield self.get_query_values(account_list)
            done = True
            message = {'accounts':unique_list}
            self.set_status(200)
        # get account list
        if not done and not account_uuid:
            message = yield self.get_account_list(account, start, end, lapse, status, page_num)
            message = {
                'count': account_list.get('response')['numFound'],
                'page': page_num,
                'results': []
            }
            for doc in account_list.get('response')['docs']:
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message['results'].append(
                    dict((key.split('_register')[0], value)
                    for (key, value) in doc.items() if key not in IGNORE_ME)
                )
            self.set_status(200)
        # single account received
        if not done and account_uuid:
            # try to get stuff from cache first
            account_uuid = account_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('accounts:{0}'.format(account_uuid))
            if message is not None:
                logging.info('accounts:{0} done retrieving!'.format(account_uuid))
                #result = data
                self.set_status(200)
            else:
                #data = yield self.get_account(account, account_uuid.rstrip('/'))
                message = yield self.get_query(account, account_uuid)
                if self.cache.add('accounts:{0}'.format(account_uuid), message, 1):
                    logging.info('new cache entry {0}'.format(str(account_uuid)))
                    self.set_status(200)
            if not message:
                self.set_status(400)
                message = {'missing account {0} account_uuid {1} page_num {2} checked {3}'.format(
                    account, account_uuid.rstrip('/'), page_num, checked):result}
        # thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def get(self, account=None, account_uuid=None, start=None, end=None, page_num=1, lapse='hours'):
        '''
            Get accounts
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_username_cookie()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # not unique
        unique = query_args.get('unique', False)
        # rage against the finite state machine
        status = 'all'
        # are we done yet?
        done = False
        # some random that crash this shit
        message = {'crashing': True}
        # unique flag activated
        if unique:
            unique_stuff = {key:query_args[key][0] for key in query_args}
            account_list = yield self.get_unique_querys(unique_stuff)
            unique_list = yield self.get_query_values(account_list)
            done = True
            message = {'accounts':unique_list}
            self.set_status(200)

        # get account list
        if not done and not account_uuid:
            account_list = yield self.get_account_list(account, start, end, lapse, status, page_num)
            message = {
                'count': account_list.get('response')['numFound'],
                'page': page_num,
                'results': []
            }
            for doc in account_list.get('response')['docs']:
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message['results'].append(
                    dict((key.split('_register')[0], value)
                    for (key, value) in doc.items() if key not in IGNORE_ME)
                )
            self.set_status(200)
        # single account received
        if not done and account_uuid:
            # try to get stuff from cache first
            account_uuid = account_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('accounts:{0}'.format(account_uuid))
            logging.info(message)
            if message is not None:
                logging.info('accounts:{0} done retrieving!'.format(account_uuid))
                #result = data
                self.set_status(200)
            else:
                #data = yield self.get_account(account, account_uuid.rstrip('/'))
                message = yield self.get_account(account, account_uuid)
                if self.cache.add('accounts:{0}'.format(account_uuid), message, 1):
                    logging.info('new cache entry {0}'.format(str(account_uuid)))
                    self.set_status(200)
            if not message:
                self.set_status(400)
                message = {'missing account {0} account_uuid {1} page_num {2} checked {3}'.format(
                    account, account_uuid.rstrip('/'), page_num, checked):result}
        # thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def post(self):
        '''
            Create account
        '''
        struct = yield check_json(self.request.body)
        format_pass = (True if struct and not struct.get('errors') else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        # request query arguments
        query_args = self.request.arguments
        # get account from new account struct
        account = struct.get('account', None)
        # get the current frontend logged username
        username = self.get_username_cookie()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # execute new account struct
        ack = yield self.new_account(struct)
        # complete message with receive acknowledgment uuid.
        message = {'uuid':ack}
        if 'error' in message['uuid']:
            scheme = 'account'
            reason = {'duplicates': [
                (scheme, 'account'),
                (scheme, 'uuid')
            ]}
            message = yield self.let_it_crash(struct, scheme, message['uuid'], reason)
            self.set_status(400)
        else:
            self.set_status(201)
        self.finish(message)

    @gen.coroutine
    def patch(self, account_uuid):
        '''
            Modify account
        '''
        struct = yield check_json(self.request.body)

        logging.warning(struct)

        logging.warning(self.request.headers)

        format_pass = (True if not dict(struct).get('errors', False) else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        account = self.request.arguments.get('account', [None])[0]
        if not account:
            # if not account we try to get the account from struct
            account = struct.get('account', None)

        logging.warning('clean this shit up')

        result = yield self.modify_account(account, account_uuid, struct)
        if not result:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('account', account_uuid)
            self.finish(error)
            return
        self.set_status(200)
        self.finish({'message': 'update completed successfully'})

    @gen.coroutine
    def delete(self, account_uuid):
        '''
            Delete account
        '''
        query_args = self.request.arguments
        account = query_args.get('account', [None])[0]
        result = yield self.remove_account(account, account_uuid)
        if not result:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('account', account_uuid)
            self.finish(error)
            return
        self.set_status(204)
        self.finish()

    @gen.coroutine
    def options(self, account_uuid=None):
        '''
            Resource options
        '''
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PATCH, DELETE, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', ''.join(('Accept-Language,',
                        'DNT,Keep-Alive,User-Agent,X-Requested-With,',
                        'If-Modified-Since,Cache-Control,Content-Type,',
                        'Content-Range,Range,Date,Etag')))
        # allowed http methods
        message = {
            'Allow': ['HEAD', 'GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS']
        }
        # resource parameters
        parameters = {}
        # mock your stuff
        stuff = models.User.get_mock_object().to_primitive()
        for k, v in stuff.items():
            if v is None:
                parameters[k] = str(type('none'))
            elif isinstance(v, unicode):
                parameters[k] = str(type('unicode'))
            else:
                parameters[k] = str(type(v))
        # after automatic madness return description and parameters
        # we now have the option to clean a little bit.
        parameters['labels'] = 'array/string'
        # end of manual cleaning
        POST = {
            "description": "Send account",
            "parameters": parameters
        }
        # filter single resource
        if not account_uuid:
            message['POST'] = POST
        else:
            message['Allow'].remove('POST')
            message['Allow'].append('PATCH')
            message['Allow'].append('DELETE')
        self.set_status(200)
        self.finish(message)


class OrgsHandler(orgs.Org, BaseHandler):
    '''
        HTTP request handlers
    '''

    @gen.coroutine
    def head(self, account=None, org_uuid=None, page_num=0):
        '''
            Head orgs
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_username_cookie()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # not unique
        unique = query_args.get('unique', False)
        # rage against the finite state machine
        status = 'all'
        # are we done yet?
        done = False
        # some random that crash this shit
        message = {'crashing': True}
        # unique flag activated
        if unique:
            unique_stuff = {key:query_args[key][0] for key in query_args}
            org_list = yield self.get_unique_queries(unique_stuff)
            unique_list = yield self.get_query_values(org_list)
            done = True
            message = {'orgs':unique_list}
            self.set_status(200)
        # get org list
        if not done and not org_uuid:
            message = yield self.get_org_list(account, start, end, lapse, status, page_num)
            message = {
                'count': org_list.get('response')['numFound'],
                'page': page_num,
                'results': []
            }
            for doc in org_list.get('response')['docs']:
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message['results'].append(
                    dict((key.split('_register')[0], value)
                    for (key, value) in doc.items() if key not in IGNORE_ME)
                )
            self.set_status(200)
        # single org received
        if not done and org_uuid:
            # try to get stuff from cache first
            org_uuid = org_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('orgs:{0}'.format(org_uuid))
            if message is not None:
                logging.info('orgs:{0} done retrieving!'.format(org_uuid))
                #result = data
                self.set_status(200)
            else:
                #data = yield self.get_org(account, org_uuid.rstrip('/'))
                message = yield self.get_query(account, org_uuid)
                if self.cache.add('orgs:{0}'.format(org_uuid), message, 1):
                    logging.info('new cache entry {0}'.format(str(org_uuid)))
                    self.set_status(200)
            if not message:
                self.set_status(400)
                message = {'missing account {0} org_uuid {1} page_num {2} checked {3}'.format(
                    account, org_uuid.rstrip('/'), page_num, checked):result}
        # thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def get(self, account=None, org_uuid=None, start=None, end=None, page_num=1, lapse='hours'):
        '''
            Get orgs
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_username_cookie()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # not unique
        unique = query_args.get('unique', False)
        # rage against the finite state machine
        status = 'all'
        # are we done yet?
        done = False
        # some random that crash this shit
        message = {'crashing': True}
        # unique flag activated
        if unique:
            unique_stuff = {key:query_args[key][0] for key in query_args}
            org_list = yield self.get_unique_querys(unique_stuff)
            unique_list = yield self.get_query_values(org_list)
            done = True
            message = {'orgs':unique_list}
            self.set_status(200)

        # get org list
        if not done and not org_uuid:
            org_list = yield self.get_org_list(account, start, end, lapse, status, page_num)
            message = {
                'count': org_list.get('response')['numFound'],
                'page': page_num,
                'results': []
            }
            for doc in org_list.get('response')['docs']:
                IGNORE_ME = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
                message['results'].append(
                    dict((key.split('_register')[0], value)
                    for (key, value) in doc.items() if key not in IGNORE_ME)
                )
            self.set_status(200)
        # single org received
        if not done and org_uuid:
            # try to get stuff from cache first
            org_uuid = org_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('orgs:{0}'.format(org_uuid))
            if message is not None:
                logging.info('orgs:{0} done retrieving!'.format(org_uuid))
                #result = data
                self.set_status(200)
            else:
                #data = yield self.get_org(account, org_uuid.rstrip('/'))
                message = yield self.get_org(account, org_uuid)
                if self.cache.add('orgs:{0}'.format(org_uuid), message, 1):
                    logging.info('new cache entry {0}'.format(str(org_uuid)))
                    self.set_status(200)
            if not message:
                self.set_status(400)
                message = {'missing account {0} org_uuid {1} page_num {2} checked {3}'.format(
                    account, org_uuid.rstrip('/'), page_num, checked):result}
        # thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def post(self):
        '''
            Create org
        '''
        struct = yield check_json(self.request.body)
        format_pass = (True if struct and not struct.get('errors') else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        # request query arguments
        query_args = self.request.arguments
        # get account from new org struct
        account = struct.get('account', None)
        # get the current frontend logged username
        username = self.get_username_cookie()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # execute new org struct
        ack = yield self.new_org(struct)
        # complete message with receive acknowledgment uuid.
        message = {'uuid':ack}
        if 'error' in message['uuid']:
            scheme = 'org'
            reason = {'duplicates': [
                (scheme, 'account'),
                (scheme, 'uuid')
            ]}
            message = yield self.let_it_crash(struct, scheme, message['uuid'], reason)
            self.set_status(400)
        else:
            self.set_status(201)
        self.finish(message)

    @gen.coroutine
    def patch(self, org_uuid):
        '''
            Modify org
        '''
        struct = yield check_json(self.request.body)
        format_pass = (True if not dict(struct).get('errors', False) else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        account = self.request.arguments.get('account', [None])[0]
        if not account:
            # if not account we try to get the account from struct
            account = struct.get('account', None)
        result = yield self.modify_org(account, org_uuid, struct)
        if not result:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('org', org_uuid)
            self.finish(error)
            return
        self.set_status(200)
        self.finish({'message': 'update completed successfully'})

    @gen.coroutine
    def delete(self, org_uuid):
        '''
            Delete org
        '''
        query_args = self.request.arguments
        account = query_args.get('account', [None])[0]
        result = yield self.remove_org(account, org_uuid)
        if not result:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('org', org_uuid)
            self.finish(error)
            return
        self.set_status(204)
        self.finish()

    @gen.coroutine
    def options(self, org_uuid=None):
        '''
            Resource options
        '''
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'HEAD, GET, POST, PATCH, DELETE, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', ''.join(('Accept-Language,',
                        'DNT,Keep-Alive,User-Agent,X-Requested-With,',
                        'If-Modified-Since,Cache-Control,Content-Type,',
                        'Content-Range,Range,Date,Etag')))
        # allowed http methods
        message = {
            'Allow': ['HEAD', 'GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS']
        }
        # resource parameters
        parameters = {}
        # mock your stuff
        stuff = models.Org.get_mock_object().to_primitive()
        for k, v in stuff.items():
            if v is None:
                parameters[k] = str(type('none'))
            elif isinstance(v, unicode):
                parameters[k] = str(type('unicode'))
            else:
                parameters[k] = str(type(v))
        # after automatic madness return description and parameters
        # we now have the option to clean a little bit.
        parameters['labels'] = 'array/string'
        # end of manual cleaning
        POST = {
            "description": "Send org",
            "parameters": parameters
        }
        # filter single resource
        if not org_uuid:
            message['POST'] = POST
        else:
            message['Allow'].remove('POST')
            message['Allow'].append('PATCH')
            message['Allow'].append('DELETE')
        self.set_status(200)
        self.finish(message)
