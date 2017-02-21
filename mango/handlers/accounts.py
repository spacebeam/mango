# -*- coding: utf-8 -*-
'''
    Mango HTTP accounts handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import time
import motor
import logging
import ujson as json
from tornado import gen
from tornado import web
from mango import errors
from mango.messages import accounts as models
from mango.system import accounts
from mango.system import records
from mango.tools import check_json
from mango.tools import new_resource
from mango.handlers import BaseHandler

from tornado import httpclient

httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')


class UsersHandler(accounts.MangoAccounts, BaseHandler):
    '''
        User accounts HTTP request handlers
    '''

    @gen.coroutine
    def head(self, account=None, page_num=0):
        '''
            Head users
        '''
        # logging request query arguments
        logging.info('request query arguments {0}'.format(self.request.arguments))
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_current_username()
        # if the user don't provide an account we use the frontend username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)
        # account type flag
        account_type = 'user'
        # status
        status = 'all'
        # cache data
        data = None
        # return result message
        result = None
        if not account:
            users = yield self.get_account_list(account_type, status, page_num)
            self.finish({'users':users})
        else:
            # try to get stuff from cache first
            logging.info('getting users:{0} from cache'.format(account))
            try:
                data = self.cache.get('users:{0}'.format(account))
            except Exception, e:
                logging.exception(e)
            if data is not None:
                logging.info('users:{0} done retrieving!'.format(account))
                result = data
            else:
                data = yield self.get_account(account.rstrip('/'), account_type)
                try:
                    if self.cache.add('users:{0}'.format(account), data, 1):
                        logging.info('new cache entry {0}'.format(str(data)))
                except Exception, e:
                    logging.exception(e)
            result = (data if data else None)
            if not result:
                # -- nead moar info
                self.set_status(400)
                self.finish({'missing':account.rstrip('/')})
            else:
                self.set_status(200)
                self.finish(result)

    @gen.coroutine
    def get(self, account=None, page_num=0):
        '''
            Get user accounts
        '''
        # logging request query arguments
        logging.info('request query arguments {0}'.format(self.request.arguments))
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_current_username()
        # if the user don't provide an account we use the frontend username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)
        # account type flag
        account_type = 'user'
        # status
        status = 'all'
        # cache data
        data = None
        # return result message
        result = None
        if not account:
            users = yield self.get_account_list(account_type, status, page_num)
            self.finish({'users':users})
        else:
            # try to get stuff from cache first
            logging.info('getting users:{0} from cache'.format(account))
            try:
                data = self.cache.get('users:{0}'.format(account))
            except Exception, e:
                logging.exception(e)
            if data is not None:
                logging.info('users:{0} done retrieving!'.format(account))
            else:
                data = yield self.get_account(account.rstrip('/'), account_type)
                try:
                    if self.cache.add('users:{0}'.format(account), data, 1):
                        logging.info('new cache entry {0}'.format(str(data)))
                except Exception, e:
                    logging.exception(e)
            result = (data if data else None)
            if not result:
                # -- need more info
                self.set_status(400)
                self.finish({'missing':account.rstrip('/')})
            else:
                self.set_status(200)
                self.finish(result)
                
    @gen.coroutine
    def post(self):
        '''
            Create user account
        '''
        struct = yield check_json(self.request.body)
        format_pass = (True if struct and not struct.get('errors') else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        struct['account_type'] = 'user'
        logging.info('new account structure %s' % str(struct))
        result = yield self.new_account(struct)
        if 'error' in result:
            model = 'User'
            reason = {'duplicates': [(model, 'account'), (model, 'email')]}
            message = yield self.let_it_crash(struct, model, result, reason)
            logging.warning(message)
            self.set_status(400)
            self.finish(message)
            return
        def handle_response(response):
            '''
                Handle response
            '''
            if response.error:
                logging.error(response.error)
            else:
                logging.info(response.body)
        # -- handle SIP account creation out-of-band <------------------- refactor this shit kind of thing.
        # postgresql insert sip account
        if result:
            data = {'password': struct['password'], 'account': struct['account']}
            # generate sip struct
            sip_account = yield self.new_sip_account(struct)
            
            # generate coturn struct
            coturn_struct = {
                'account': struct['account'],
                'labels': ['coturn',],
                'title': 'confirm coturn account',
                'payload': json.dumps(data)
            }
            # yield the new stuff up
            coturn_account = yield self.new_coturn_account(coturn_struct)
            http_client = httpclient.AsyncHTTPClient()
            http_client.fetch(
                'https://iofun.io/fire/', 
                headers={"Content-Type": "application/json"},
                method='POST',
                body=json.dumps({'username': struct['account'], 'password': struct['password']}),
                callback=handle_response
            )
            logging.info(coturn_account)
        self.set_status(201)
        self.finish({'uuid':result})

    @gen.coroutine
    def patch(self, account):
        '''
            Update user account
        '''

        logging.info('request.arguments {0}'.format(self.request.arguments))
        logging.info('request.body {0}'.format(self.request.body))
        struct = yield check_json(self.request.body)
        logging.info('patch received struct {0}'.format(struct))
        format_pass = (True if struct and not struct.get('errors') else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        struct['account_type'] = 'user'
        logging.info('new update on account structure %s' % str(struct))
        MISSING_ACCOUNT_UUID = None
        result = yield self.modify_account(account, MISSING_ACCOUNT_UUID, struct)
        logging.info(result)
        if not result:
            message = 'update failed something is bananas'
            self.set_status(400)
        else:
            message = 'update completed successfully'
            self.set_status(200)
        self.finish({'message': message})

    @gen.coroutine
    def delete(self, account):
        '''
            Delete a user account
        '''
        account = account.rstrip('/')
        result = yield self.remove_account(account)
        logging.info("why result['n'] ? %s" % str(result))
        if not result['n']:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('user', account)
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
        self.set_header('Access-Control-Allow-Headers',
                        'DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range,Date,Etag')
        message = {
            'Allow': ['HEAD', 'GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS']
        }
        # resource parameters
        parameters = {}
        # mock stuff
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
            "description": "Create user",
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


class OrgsHandler(accounts.Orgs, BaseHandler):
    '''
        Organization account resource handlers
    '''

    @gen.coroutine
    def head(self, account=None, page_num=0):
        '''
            Organization accounts head

        '''
        # logging request query arguments
        logging.info('request query arguments {0}'.format(self.request.arguments))
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_current_username()
        # status
        status = 'all'
        # get the current frontend context account
        #organization = self.get_current_org()
        # if the user don't provide an account we use the frontend username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)
        account_type = 'org'
        if not account:
            orgs = yield self.get_account_list(account_type, status, page_num) 
            self.finish({'orgs':orgs})
        else:
            # try to get stuff from cache first
            logging.info('getting orgs:{0} from cache'.format(account))
            data = self.cache.get('orgs:{0}'.format(account))
            if data is not None:
                logging.info('orgs:{0} done retrieving!'.format(account))
                result = data
            else:
                data = yield self.get_account(account.rstrip('/'), account_type)
                if self.cache.add('orgs:{0}'.format(account), data, 1):
                    logging.info('new cache entry {0}'.format(str(data)))
                    result = data
            #result = yield self.get_account(account, account_type)
            if not result:
                # -- need moar info
                self.set_status(400)
                self.finish({'missing':account})
            else:
                self.set_status(200)
                self.finish(result)

    @gen.coroutine
    def get(self, account=None, page_num=0):
        '''
            Get organization accounts
        '''
        # logging request query arguments
        logging.info('request query arguments {0}'.format(self.request.arguments))
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend logged username
        username = self.get_current_username()
        # get the current frontend context account
        #organization = self.get_current_org()
        status = 'all'
        # if the user don't provide an account we use the frontend username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)
        account_type = 'org'
        if not account:
            orgs = yield self.get_account_list(account_type, status, page_num) 
            self.finish({'orgs':orgs})
        else:
            # try to get stuff from cache first
            logging.info('getting orgs:{0} from cache'.format(account))
            data = self.cache.get('orgs:{0}'.format(account))
            if data is not None:
                logging.info('orgs:{0} done retrieving!'.format(account))
                result = data
            else:
                data = yield self.get_account(account.rstrip('/'), account_type)
                if self.cache.add('orgs:{0}'.format(account), data, 1):
                    logging.info('new cache entry {0}'.format(str(data)))
                    result = data
            #result = yield self.get_account(account, account_type)
            if not result:
                self.set_status(400)
                self.finish({'missing':account})
            else:
                self.set_status(200)
                self.finish(result)

    @gen.coroutine
    def post(self):
        '''
            Create organization accounts
        '''
        logging.info('hola hola hola hola')
        struct = yield check_json(self.request.body)
        logging.error(struct)
        struct['account_type'] = 'org'
        org = struct['account']
        format_pass = (True if struct and not struct.get('errors') else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return
        # logging new contact structure
        logging.info('new contact structure {0}'.format(str(struct)))
        # logging request query arguments
        logging.info(self.request.arguments)
        # request query arguments
        query_args = self.request.arguments
        # get owner account from new org struct
        owner_user = struct.get('owner', None)
        # get the current frontend logged username
        username = self.get_current_username()
        # last but not least, we check query_args for owner
        owner_user = (query_args.get('owner', [username])[0] if not owner_user else owner_user)
        # we use the front-end username as last resort
        #if not struct.get('owner'):
        #    struct['owner'] = owner_user
        new_org = yield self.new_account(struct)
        if 'error' in new_org:
            scheme = 'org'
            reason = {'duplicates':[
                (scheme, 'account'),
                (scheme, 'email')
            ]}
            message = yield self.let_it_crash(struct, scheme, new_org, reason)
            logging.warning(message)
            self.set_status(400)
            self.finish(message)
            return
        team = {
            'name': 'owners',
            'permission': 'admin',
            'members': [owner_user]
        }
        check_member, check_team = yield [
            self.new_member(org, owner_user),
            self.new_team(org, team)
        ]
        self.set_status(201)
        self.finish({'uuid':new_org})

    @gen.coroutine
    def delete(self, account):
        '''       
            Delete organization account
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
        logging.info('check for n stuff %s' % (result))
        if not result['n']:
            self.set_status(400)
            system_error = errors.Error('missing')
            error = system_error.missing('org', org)
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
        self.set_header('Access-Control-Allow-Headers',
                        'DNT,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Content-Range,Range,Date,Etag')
        message = {
            'Allow': ['HEAD', 'GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS']
        }
        # resource parameters
        parameters = {}
        # mock stuff
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
            "description": "Create org",
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

