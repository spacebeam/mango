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

import queries

import logging

from tornado import gen
from tornado import web

from zmq.eventloop import ioloop

from mango.system import basic_authentication

from mango.tools import check_account_authorization
from mango.tools import errors

from mango.tools.quotes import PeopleQuotes


# msg means message

# dht means distributed hash table

# share hash table missing.

def spawn(message):
    '''
        Spawn process, return new uuid
    '''
    print("Spawn process {0}".format(message))

def link(message):
    '''
        Link processes
    '''
    print("Link processes {0}".format(message))

def spawn_link(message):
    '''
        Spawn link processes
    '''
    print("Spawn new process, {0} return Received process uuid".format(message))

def register(message):
    '''
        Register process uuid
    '''
    print("Received message: %s" % message)

def get_command(message):
    print("Received control command: %s" % message)
    if message[0] == "Exit":
        print("Received exit command, client will stop receiving messages")
        should_continue = False
        ioloop.IOLoop.instance().stop()
        
def process_message(message):
    print("Processing ... %s" % message)

def context_switch(message):
    '''
        Node context switch
    '''
    print("talk between nodes")


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
    def cache(self):
        '''
            Cache backend
        '''
        return self.settings['cache']

    def initialize(self, **kwargs):
        '''
            Initialize the Base Handler
        '''
        # Service Process Quality Management
        #===================================

        # The Senate and People of Mars
        # -----------------------------
        # SPQM communication message clannels.

        # 0MQ message channels
        # --------------------

        # CDR stream
        # self.cdr_stream = self.settings['cdr_stream']

        # CDR periodic channel
        # self.cdr_periodic = self.settings['cdr_periodic']


        super(BaseHandler, self).initialize(**kwargs)

        self.etag = None

        # System database
        self.db = self.settings['db']

        # Page settings
        self.page_size = self.settings['page_size']

    def set_default_headers(self):
        '''
            Mango default headers
        '''
        # if debug set allow all if not set settings domain
        self.set_header("Access-Control-Allow-Origin", '*')
        # self.set_header("Access-Control-Allow-Origin", self.settings['domain'])

    def get_current_username(self):
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
    def let_it_crash(self, struct, scheme, error, reason):
        '''
            Let it crash.
        '''

        str_error = str(error)
        error_handler = errors.Error(error)
        messages = []

        if error and 'Model' in str_error:
            message = error_handler.model(scheme)

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
            # Get SQL database from mango settings
            sql = self.settings.get('sql')
            # PostgreSQL insert new sip account query
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
                    '{0}',
                    '{1}',
                    '{2}',
                    '{3}',
                    'dynamic',
                    '{4}',
                    'ulaw,alaw,g729,gsm',
                    'fun-accounts',
                    'no',
                    'no'
                );
            '''.format(
                struct.get('account'),
                struct.get('account'),
                struct.get('account'),
                struct.get('domain', self.settings.get('domain')),
                struct.get('password')
            )
            result = yield sql.query(query)

            if result:
                message = {'ack': True}
            else:
                message = {'ack': False}

            result.free()

            logging.warning('new sip account spawned on PostgreSQL {0}'.format(message))

        # TODO: Still need to check the follings exceptions with the new queries module.
        #except (psycopg2.Warning, psycopg2.Error) as e:
        #    logging.exception(e)
        #    raise e
        
        except Exception, e:
            logging.exception(e)
            raise e

        raise gen.Return(message)


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

    @gen.coroutine
    def options(self):
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
