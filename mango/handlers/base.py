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


import motor

from tornado import gen
from tornado import web

from mango.tools import errors

from mango.system import basic_authentication
from mango.tools import check_account_authorization


class MangoBaseHandler(web.RequestHandler):
    '''
        Mango Base Handler
    '''

    @property
    def sql(self):
        '''
            SQL database
        '''
        return self.database.sql

    @property
    def document(self):
        '''
            document database
        '''
        return self.database.document

    @property
    def kvalue(self):
        '''
            key-value database
        '''
        return self.database.kvalue

    @property
    def graph(self):
        '''
            graph database
        '''
        return self.database.graph
    
    def initialize(self, **kwargs):
        ''' 
            Initialize the Base Handler
        '''
        super(MangoBaseHandler, self).initialize(**kwargs)

        self.etag = None
        
        self.database = None
        
        # Mongodb database
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
    

class HomeHandler(MangoBaseHandler):
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
class MangoLoginHandler(MangoBaseHandler):
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


class MangoLogoutHandler(MangoBaseHandler):
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