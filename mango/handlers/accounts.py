# This file is part of mango.

# Distributed under the terms of the last AGPL License.


__author__ = 'Jean Chassoul'


import logging
from tornado import gen
from mango.schemas import accounts as models
from mango.system import accounts
from mango.tools import str2bool, check_json
from mango.handlers import BaseHandler
from collections import OrderedDict


class UsersHandler(accounts.Accounts, BaseHandler):
    '''
        HTTP request handlers
    '''

    @gen.coroutine
    def head(self,
             account=None,
             user_uuid=None,
             start=None,
             end=None,
             lapse='hours',
             page_num=1):
        '''
            Get user accounts
        '''
        # request query arguments
        query_args = self.request.arguments
        username = False  # TODO: get the username from a front-end token!
        # if the user don't provide an account use the username as last resort
        account = (query_args.get('account', [username])[0]
                   if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        logging.info('Why? what are u checking? {0}'.format(checked))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # rage against the state machine
        status = 'all'  # TODO: Why 'all' ?
        # init message on error
        message = {'error': True}
        # init status that match with our message
        self.set_status(400)
        # check if we're list processing
        if not user_uuid:
            # TODO: missing account, start, end, lapse and status support!
            message = yield self.get_user_list(account,
                                               start,
                                               end,
                                               lapse,
                                               status,
                                               page_num)
            self.set_status(200)
        else:
            user_uuid = user_uuid.rstrip('/')
            message = yield self.get_user(account, user_uuid)
            self.set_status(200)
        # so long and thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def get(self,
            account=None,
            user_uuid=None,
            start=None,
            end=None,
            lapse='hours',
            page_num=1):
        '''
            Get user accounts
        '''
        # request query arguments
        query_args = self.request.arguments
        username = False  # TODO: get the username from a front-end token!
        # if the user don't provide an account use the username as last resort
        account = (query_args.get('account', [username])[0]
                   if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        logging.info('Why? what are u checking? {0}'.format(checked))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # rage against the state machine
        status = 'all'  # TODO: Why 'all' ?
        # init message on error
        message = {'error': True}
        # init status that match with our message
        self.set_status(400)
        # check if we're list processing
        if not user_uuid:
            # TODO: missing account, start, end, lapse and status support!
            message = yield self.get_user_list(account,
                                               start,
                                               end,
                                               lapse,
                                               status,
                                               page_num)
            self.set_status(200)
        else:
            user_uuid = user_uuid.rstrip('/')
            message = yield self.get_user(account, user_uuid)
            self.set_status(200)
        # so long and thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def post(self):
        '''
            Create user account
        '''
        struct = yield check_json(self.request.body)
        format_pass = (True if struct and not struct.get('errors') else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON': format_pass})
            return
        # create new user struct
        user_uuid = yield self.new_game(struct)
        # complete message with receive uuid.
        message = {'uuid': user_uuid}
        self.set_status(201)
        self.finish(message)

    @gen.coroutine
    def patch(self, user_uuid):
        '''
            Modify user
        '''
        struct = yield check_json(self.request.body)
        format_pass = (True if struct and not struct.get('errors') else False)
        message = {'message': 'not found'}
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON': format_pass})
            return
        account = self.request.arguments.get('account', [None])[0]
        if not account:
            # if not account we try to get the account from struct
            account = struct.get('account', None)
        result = yield self.modify_user(account, user_uuid, struct)
        if not result:
            self.set_status(400)
            self.finish(message)
            return
        self.set_status(400)
        message = {'message': 'update completed successfully'}
        self.finish(message)

    @gen.coroutine
    def delete(self, user_uuid):
        '''
            Delete user
        '''
        query_args = self.request.arguments
        account = query_args.get('account', [None])[0]
        result = yield self.remove_account(account, user_uuid)
        if not result:
            self.set_status(400)
            message = {'message': 'Error something was wrong!'}
            self.finish(message)
            return
        self.set_status(204)
        self.finish()

    @gen.coroutine
    def options(self, user_uuid=None):
        '''
            Resource options
        '''
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods',
                        'HEAD, GET, POST, PATCH, DELETE, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        ''.join(
                            ('Accept-Language,',
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
        stuff = False
        while not stuff:
            try:
                stuff = models.User.get_mock_object().to_primitive()
            except Exception as error:
                logging.warning(error)
                pass
        for k, v in stuff.items():
            if v is None:
                parameters[k] = str(type('none'))[1:-1].split(' ')[1][1:-1]
            else:
                parameters[k] = str(type(v))[1:-1].split(' ')[1][1:-1]
        # after automatic madness return description and parameters
        parameters['labels'] = 'list/object'
        parameters['orgs'] = 'list/object'
        parameters['teams'] = 'list/object'
        # end of manual cleaning
        POST = {
            "description": "Create a new user account",
            "parameters": OrderedDict(
                sorted(parameters.items(), key=lambda t: t[0]))
        }
        # filter single resource
        if not user_uuid:
            message['POST'] = POST
        else:
            message['Allow'].remove('POST')
            message['Allow'].append('PATCH')
            message['Allow'].append('DELETE')
        self.set_status(200)
        self.finish(message)


class OrgsHandler(accounts.Accounts, BaseHandler):
    '''
        HTTP request handlers
    '''

    @gen.coroutine
    def head(self,
             account=None,
             org_uuid=None,
             start=None,
             end=None,
             lapse='hours',
             page_num=1):
        '''
            Get (ORG)
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend username from token
        username = self.get_username_token()
        # if the user don't provide an account we use the frontend username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # rage against the finite state machine
        status = 'all'
        # init message on error
        message = {'error':True}
        # init status that match with our message
        self.set_status(400)
        # check if we're list processing
        if not org_uuid:
            message = yield self.get_account_list(account,
                                                  start,
                                                  end,
                                                  lapse,
                                                  status,
                                                  page_num)
            self.set_status(200)
        # single org received
        else:
            # first try to get stuff from cache
            org_uuid = org_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('orgs:{0}'.format(org_uuid))
            if message is not None:
                logging.info('orgs:{0} done retrieving!'.format(org_uuid))
                self.set_status(200)
            else:
                message = yield self.get_account(account, org_uuid)
                if self.cache.add('orgs:{0}'.format(org_uuid), message, 1):
                    logging.info('new cache entry {0}'.format(str(org_uuid)))
                    self.set_status(200)
        # so long and thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def get(self,
            account=None,
            org_uuid=None,
            start=None,
            end=None,
            lapse='hours',
            page_num=1):
        '''
            Get (ORG)
        '''
        # request query arguments
        query_args = self.request.arguments
        # get the current frontend username from token
        username = self.get_username_token()
        # if the user don't provide an account we use the frontend username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)
        # query string checked from string to boolean
        checked = str2bool(str(query_args.get('checked', [False])[0]))
        # getting pagination ready
        page_num = int(query_args.get('page', [page_num])[0])
        # rage against the finite state machine
        status = 'all'
        # init message on error
        message = {'error':True}
        # init status that match with our message
        self.set_status(400)
        # check if we're list processing
        if not org_uuid:
            message = yield self.get_org_list(account,
                                              start,
                                              end,
                                              lapse,
                                              status,
                                              page_num)
            self.set_status(200)
        # single org received
        else:
            # first try to get stuff from cache
            org_uuid = org_uuid.rstrip('/')
            # get cache data
            message = self.cache.get('orgs:{0}'.format(org_uuid))
            if message is not None:
                logging.info('cache orgs:{0} done retrieving!'.format(org_uuid))
                self.set_status(200)
            else:
                message = yield self.get_org(account, org_uuid)
                if self.cache.add('orgs:{0}'.format(org_uuid), message, 1):
                    logging.info('new cache entry {0}'.format(str(org_uuid)))
                    self.set_status(200)
        # so long and thanks for all the fish
        self.finish(message)

    @gen.coroutine
    def post(self):
        '''
            Create (ORG)
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
        # get the current frontend username from token
        username = self.get_username_token()
        # if the user don't provide an account we use the username
        account = (query_args.get('account', [username])[0] if not account else account)
        # execute new org struct
        org_uuid = yield self.new_org(struct)
        # add_org to user -> the struct['account'] here is the org_account
        new_org = yield self.add_org(struct['created_by'], struct['account'], org_uuid)
        # complete message with receive uuid.
        message = {'uuid':org_uuid}
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
            Modify (ORG)
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
        # remove query string flag
        remove = self.request.arguments.get('remove', False)
        if not remove :
            result = self.cache.delete('org:{0}'.format(org_uuid))
            result = yield self.modify_account(account, org_uuid, struct)
        else:
            result = self.cache.delete('org:{0}'.format(org_uuid))
            result = yield self.modify_remove(account, org_uuid, struct)
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
            Delete (ORG)
        '''
        query_args = self.request.arguments
        account = query_args.get('account', [None])[0]
        result = yield self.remove_account(account, org_uuid)
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
        stuff = False
        while not stuff:
            try:
                stuff = models.Org.get_mock_object().to_primitive()
            except Exception as error:
                pass
        for k, v in stuff.items():
            if v is None:
                parameters[k] = str(type('none'))
            else:
                parameters[k] = str(type(v))
        # after automatic madness return description and parameters
        parameters['labels'] = 'array/string'
        parameters['members'] = 'array/string'
        parameters['teams'] = 'array/kv/string'
        # end of manual cleaning
        POST = {
            "description": "Create (ORG)",
            "parameters": OrderedDict(sorted(parameters.items(), key=lambda t: t[0]))
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
