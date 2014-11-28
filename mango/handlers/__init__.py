# -*- coding: utf-8 -*-
'''
    Mango HTTP base handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import time
import motor

import psycopg2
import momoko

import logging

from tornado import gen
from tornado import web

from mango.system import basic_authentication

from mango.tools import check_account_authorization
from mango.tools import errors

from mango.tools.quotes import PeopleQuotes


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
        return self.settings['sql']

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
        return self.application.graph

    def initialize(self, **kwargs):
        '''
            Initialize the Base Handler
        '''
        # Service Process Quality Management

        super(BaseHandler, self).initialize(**kwargs)

        self.etag = None

        # System database
        self.db = self.settings['db']

        # The Senate and People of Mars
        # -----------------------------
        # communication message clannels.

        # 0MQ message channels
        # --------------------

        # SPQM 

        # CDR stream
        # self.cdr_stream = self.settings['cdr_stream']

        # CDR periodic channel
        # self.cdr_periodic = self.settings['cdr_periodic']

        # Page settings
        self.page_size = self.settings['page_size']

    def set_default_headers(self):
        '''
            Mango default headers
        '''
        # if debug set allow all if not set settings domain
        self.set_header("Access-Control-Allow-Origin", '*')
        # self.set_header("Access-Control-Allow-Origin", self.settings['domain'])

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

    @gen.coroutine
    def let_it_crash(self, struct, model, error, reason):
        '''
            Let it crash.
        '''

        str_error = str(error)
        error_handler = errors.Error(error)
        messages = []

        if error and 'Model' in str_error:
            message = error_handler.model(model)

        elif error and 'duplicate' in str_error:
            
            for name, value in reason.get('duplicates'):

                if value in str_error:

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
            logging.warning(str_error)
            
            message = {
                'error': u'nonsense',
                'message': u'there is no error'
            }

        else:
            quotes = PeopleQuotes()
            
            message = {
                'status': 200,
                'message': quotes.get()
            }

        raise gen.Return(message)

    @gen.coroutine
    def new_sip_account(self, struct):
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
                    'ulaw,alaw,g729,gsm',
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

        except (psycopg2.Warning, psycopg2.Error) as e:
            logging.exception(e)
            raise e
        else:
            result = True

        raise gen.Return(result)


@basic_authentication
class LoginHandler(BaseHandler):
    '''
        BasicAuth login
    '''

    @gen.coroutine
    def get(self):
        # redirect next url
        next_url = '/'
        args = self.get_arguments('next')
        if args:
            next_url = args[0]

        account = yield check_account_authorization(self.db,
                            self.username,
                            self.password)

        if not account:
            # 401 status code?
            self.set_status(403)
            # dude! get realm from options.
            self.set_header('WWW-Authenticate', 'Basic realm=mango')
            self.finish()
        else:
            self.set_secure_cookie('username', self.username)
            self.username, self.password = (None, None)

            # self.redirect(next_url)

            self.set_status(200)
            self.finish()


class LogoutHandler(BaseHandler):
    '''
        BasicAuth logout
    '''

    @gen.coroutine
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

    @gen.coroutine
    def get(self):
        '''
            Get some quotes
        '''
        quotes = PeopleQuotes()

        self.finish(
            {'quote': quotes.get()}
        )