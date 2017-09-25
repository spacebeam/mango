# -*- coding: utf-8 -*-
'''
    Mango HTTP base handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


from tornado import gen
from tornado import web
from mango.system import basic_authentication
from mango.messages import tasks as _tasks
from mango.tools import clean_structure, validate_uuid4
from mango.tools import get_account_labels, get_account_uuid
from mango import errors
import logging


class BaseHandler(web.RequestHandler):
    '''
        gente d'armi e ganti
    '''
    @property
    def kvalue(self):
        '''
            Key-value database
        '''
        return self.settings['kvalue']

    def initialize(self, **kwargs):
        '''
            Initialize the Base Handler
        '''
        super(BaseHandler, self).initialize(**kwargs)
        # System database
        self.db = self.settings.get('db')
        # System cache
        self.cache = self.settings.get('cache')
        # Page settings
        self.page_size = self.settings.get('page_size')
        # solr riak
        self.solr = self.settings.get('solr')

    def set_default_headers(self):
        '''
            mango default headers
        '''
        self.set_header("Access-Control-Allow-Origin", self.settings.get('domain', '*'))

    def get_username_cookie(self):
        '''
            Return the username from a secure cookie (require cookie_secret)
        '''
        return self.get_secure_cookie('username')

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
        raise gen.Return(message)

@basic_authentication
class LoginHandler(BaseHandler):
    '''
        BasicAuth login
    '''
    @gen.coroutine
    def get(self):
        uuid = yield get_account_uuid(self,
                            self.username,
                            self.password)
        # clean message
        message = {}
        message['labels'] = yield get_account_labels(self, self.username)
        #logging.info(uuid)
        if validate_uuid4(uuid):
            self.set_header('Access-Control-Allow-Origin','*')
            self.set_header('Access-Control-Allow-Methods','GET, OPTIONS')
            self.set_header('Access-Control-Allow-Headers','Content-Type, Authorization')
            self.set_secure_cookie('username', self.username)
            #logging.info("I've just generated a username secure cookie for {0}".format(self.username))
            # if labels we make some fucking labels
            labels = str(message['labels'])
            # labels, labels, labels
            self.set_secure_cookie('labels', labels)
            message['uuid'] = uuid
            self.username, self.password = (None, None)
            self.set_status(200)
            self.finish(message)
        else:
            # 401 status code ?
            # I don't know, why 401 ?
            self.set_status(403)
            self.set_header('WWW-Authenticate', 'Basic realm=mango')
            self.finish()
            
    @gen.coroutine
    def options(self):
        self.set_header('Access-Control-Allow-Origin','*')
        self.set_header('Access-Control-Allow-Methods','GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers','Content-Type, Authorization')
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
        self.clear_cookie('labels')
        self.set_status(200)
        self.finish()