# -*- coding: utf-8 -*-
'''
    Mango HTTP accounts handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import time
import motor
import logging
import ujson as json
from tornado import gen
from tornado import web
from mango import errors
from mango.system import accounts
from mango.system import records
from mango.tools import content_type_validation
from mango.tools import check_json
from mango.tools import new_resource
from mango.handlers import BaseHandler

from tornado import httpclient

httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')


@content_type_validation
class UsersActiveHandler(accounts.MangoAccounts, BaseHandler):
    '''
        User active accounts HTTP request handlers
    '''

    @gen.coroutine
    def get(self, page_num=0):
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
        account = (query_args.get('account', [username])[0] if not account else None)

        # account type flag
        account_type = 'user'

        # status
        status = 'all'

        users = yield self.get_account_list(account_type, status, page_num)

        self.set_status(200)
        self.finish({'users':users})


@content_type_validation
class UsersDisableHandler(accounts.MangoAccounts, BaseHandler):
    '''
        User disable accounts HTTP request handlers
    '''
    pass


@content_type_validation
class UsersSuspendedHandler(accounts.MangoAccounts, BaseHandler):
    '''
        User suspended accounts HTTP request handlers
    '''
    pass


@content_type_validation
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
            
            #result = yield self.get_account(account.rstrip('/'), account_type)

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

        # -- handle SIP account creation out-of-band <--------------------------------------- refactor this shit kind of thing.

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
                'data': json.dumps(data)
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


@content_type_validation
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

        #status
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
    
    @gen.coroutine
    def get(self, account, page_num=0):
        '''
            Get members
        '''
        logging.warning('get member')


@content_type_validation
class MembershipsHandler(accounts.Orgs, BaseHandler):
    '''
        Memberships resource handlers
    '''

    @gen.coroutine
    def get(self, account, page_num=0):
        '''
            Get organization membership/s.
        '''
        logging.info(
            'account %s page num %s.' % (account, page_num)
        )

    @gen.coroutine
    def put(self, account):
        '''
            Add or update organization membership
        '''
        struct = yield check_json(self.request.body)

        format_pass = (True if struct and not struct.get('errors') else False)
        if not format_pass:
            self.set_status(400)
            self.finish({'JSON':format_pass})
            return

        # setting database
        db = self.settings.get('db')

        # logging new contact structure
        logging.info('put organization membership structure {0}'.format(format_pass))

        # request query arguments
        query_args = self.request.arguments

        # get account from struct
        account = struct.get('account', None)

        # get the current gui username
        username = self.get_current_username()

        # if the user don't provide an account we use the username as last resort
        account = (query_args.get('account', [username])[0] if not account else account)

        # we use the front-end username as last resort
        if not struct.get('account'):
            struct['account'] = account

        logging.warning('confirm permission for this account {0}'.format(struct.get('account')))

        struct.pop('account', None)

        new_membership = yield self.new_membership(struct)

        new_membership.pop('created', None)

        if not new_membership:

            self.set_status(400)
            return

        self.set_status(201)
        self.finish(new_membership)

    @gen.coroutine
    def delete(self, account, user):
        '''
            Delete membership
        '''

        result = yield self.remove_member(account, user)

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


@content_type_validation
class RecordsHandler(accounts.Accounts, records.Records, BaseHandler):
    '''
        Records resource handlers
    '''

    @gen.coroutine
    def get(self, account, page_num=0):
        '''
            Get records handler
        '''
        logging.info(
            'accounts records handler account %s member of %s orgs.' % (account, orgs)
        )
        # check_type account with organizations
        #account_type = yield self.check_type(account, 'user')
        
        orgs = yield self.get_orgs_list(account)
                
        #if not account_type:
        #    system_error = errors.Error('invalid')
        #    self.set_status(400)
        #    error = system_error.invalid('user', account)
        #    self.finish(error)
        #    return

        result = yield self.get_record_list( 
            account=account, 
            page_num=page_num,
            lapse=None,
            start=None,
            end=None
        )

        self.finish(result)

    @gen.coroutine
    def post(self, account):
        '''
            Post records handler
        '''
        struct = yield check_json(self.request.body)
        db = self.settings['db']

        format_pass = (True if struct and not struct.get('errors') else False)
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

        resource = {
            'account': account,
            'resource': 'records',
            'uuid': record
        }

        update = yield new_resource(db, resource)

        # logging new resource update
        logging.info('update %s' % update)

        if not update:
            logging.warning(
                'account: %s new_resource record: %s update.' % (account, record)
            )

        self.set_status(201)
        self.finish({'uuid':record})


@content_type_validation
class RoutesHandler(accounts.Accounts, BaseHandler):
    '''
        Routes resource handlers
    '''
    
    @gen.coroutine
    def get(self, account):
        # get account the record billing routes from the database
        routes = yield self.get_route_list(account)
        self.finish(routes)

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

        logging.info('routes handler struct? %s' % (struct))
                
        result = yield self.new_route(struct)

        self.finish()