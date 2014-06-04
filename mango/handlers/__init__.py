# -*- coding: utf-8 -*-
'''
    Mango HTTP base handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


# Remember Gabo Naum
# http://www.youtube.com/watch?v=2k-JGuhyqKE

# accounts: {users or/and orgs}

# teams: {users members of orgs teams}

# groups: {users members of orgs groups}

# resources: {records, reports, billing}

import motor

#import psycopg2
#import momoko

from tornado import gen
from tornado import web

from mango.system import basic_authentication

from mango.tools import check_account_authorization
from mango.tools import errors

from mango.tools.quotes import HackerQuotes


class BaseHandler(web.RequestHandler):
    '''
        System application request handler

        gente d'armi e ganti
    '''

    @property
    def sql(self):
        '''
            SQL database
        '''
        return self.application.sql

    @property
    def document(self):
        '''
            Document database
        '''
        return self.application.document

    @property
    def kvalue(self):
        '''
            Key-value database
        '''
        return self.application.kvalue

    @property
    def graph(self):
        '''
            Graph database
        '''
        # Neo4j
        return self.application.graph

    def initialize(self, **kwargs):
        '''
            Initialize the Base Handler
        '''
        super(BaseHandler, self).initialize(**kwargs)

        self.etag = None

        # System database
        self.db = self.settings['db']

        # 0MQ Greatness Stuff

        # self.cdr_stream = self.settings['cdr_stream']

        # Tornado CDR periodic callbacks
        # self.cdr_periodic = self.settings['cdr_periodic']

        # Pagination settings
        self.page_size = self.settings['page_size']

    def set_default_headers(self):
        '''
            Mango default headers
        '''
        self.set_header("Access-Control-Allow-Origin", self.settings['domain'])

    def get_current_user(self):
        '''
            Return the username from a secure cookie
        '''
        return self.get_secure_cookie('username')

    def get_current_account(self):
        '''
            Return the account from a secure cookie
        '''
        return self.get_secure_cookie('account')

    @gen.engine
    def crash_and_die(self, struct, model, error, reason, callback):
        '''
            Crash the system
        '''
        str_error = str(error)
        error_handler = errors.Error(error)

        if error and 'Model' in str_error:
            message = error_handler.model(model)

        elif error and 'duplicate' in str_error:

            messages = []

            for name, value in reason.get('duplicates'):

                message = error_handler.duplicate(
                    name.title(),
                    value,
                    struct.get(value)
                )

                messages.append(message)

            message = ({'messages':messages} if messages else False)

        elif error and 'value' in str_error:
            message = error_handler.value()

        elif error is not None:

            print(type(error))
            print(error)
            print('WARNING: ', str_error, ' random nonsense.') 

            message = {
                'error': u'nonsense',
                'message': u'there is no error'
            }

        else:
            quotes = HackerQuotes()
            message = {
                'status': 200,
                'message': quotes.get()
            }

        callback(message, None)

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
                    '%s',
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
                   self.settings['domain'],
                   struct['password'])

            cursor = yield momoko.Op(self.sql.execute, query)

        except (psycopg2.Warning, psycopg2.Error) as error:
            print('WARNING: ', str(error))
            callback(None, str(error))
            return
        else:
            result = True

        callback(result, None)


@basic_authentication
class LoginHandler(BaseHandler):
    '''
        BasicAuth login
    '''

    @web.asynchronous
    @gen.engine
    def get(self):
        # redirect this shit out?
        next_url = '/'
        args = self.get_arguments('next')
        if args:
            next_url = args[0]

        account = yield motor.Op(check_account_authorization,
                                 self.db,
                                 self.username,
                                 self.password)

        if not account:
            # 401?
            self.set_status(403)
            self.set_header('WWW-Authenticate', 'Basic realm=mango')
            self.finish()
        else:
            self.set_secure_cookie('username', self.username)
            self.username, self.password = (None, None)

            # redirect where and why?
            # self.redirect(next_url)

            self.set_status(200)
            self.finish()


class LogoutHandler(BaseHandler):
    '''
        BasicAuth logout
    '''

    @web.asynchronous
    def get(self):
        '''
            Clear secure cookie
        '''
        self.clear_cookie('username')

        self.set_status(200)
        self.finish()


class MangoHandler(BaseHandler):
    '''
        Mango Handler Quote experiment
    '''

    @web.asynchronous
    def get(self):
        '''
            Get some quotes
        '''
        quotes = HackerQuotes()

        self.finish(
            {'quote': quotes.get()}
        )