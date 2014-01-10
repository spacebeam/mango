# -*- coding: utf-8 -*-
'''
    Mango base handlers
'''
# This file is part of mango.
#
# Distributed under the terms of the last AGPL License. The full
# license is in the file LICENCE, distributed as part of this
# software.

__author__ = 'Jean Chassoul'


# Remember Gabo Naum.
# http://www.youtube.com/watch?v=2k-JGuhyqKE


import motor

from tornado import gen
from tornado import web

from mango.tools import errors

from mango.system import basic_authentication
from mango.tools import check_account_authorization

# TODO: Change username to the more general account variable name.


class BaseHandler(web.RequestHandler):
    '''
        Mango Base Handler
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
            document database
        '''
        return self.application.document

    @property
    def kvalue(self):
        '''
            key-value database
        '''
        return self.application.kvalue

    @property
    def graph(self):
        '''
            graph database
        '''
        return self.application.graph
    
    def initialize(self, **kwargs):
        ''' 
            Initialize the Base Handler
        '''
        super(BaseHandler, self).initialize(**kwargs)

        self.etag = None
        
        # system database
        self.db = self.settings['db']

        # ZeroMQ streams
        # self.cdr_stream = self.settings['cdr_stream']

        # Tornado CDR periodic callbacks
        # self.cdr_periodic = self.settings['cdr_periodic']

        # Pagination settings
        self.page_size = self.settings['page_size']

    def set_default_headers(self):
        '''
            Mango default headers
        '''
        self.set_header("Access-Control-Allow-Origin", "ph3nix.com")
    
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
    

class HomeHandler(BaseHandler):
    '''
        Mango HomeHandler Quote experiment
    '''
    
    @web.asynchronous
    def get(self):
        '''
            Get some quotes
        '''
        hackers = quotes.Quotes()
        self.write({'quote': hackers.get()})
        self.finish()


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