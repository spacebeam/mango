# -*- coding: utf-8 -*-
'''
    Manage Asynchronous Number of Granular/Going ORGs
    
    Organizations of restricted generality (ORGs)
'''


# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

# Mango manage, measure and gives new meaning to ORGs data records.

# Organizations of restricted generality (ORGs) provide foundations 
# for the development of scalable, robust, and private applications.


__author__ = 'Jean Chassoul'

import os

from tornado import ioloop
from tornado import gen
from tornado import web

# from tornado import websocket

from mango.handlers import HomeHandler, LoginHandler, LogoutHandler
from mango.handlers import accounts
from mango.handlers import billings
from mango.handlers import records

from mango.tools import options
from mango.tools import indexes
from mango.tools import periodic

import logging

import arrow

import pytz

import motor

import psycopg2

import momoko


# Mango HTTP Requests

# [ Get ]
#
# GET /records/record/keys/key 


# [ Store ]
#
# POST /records/record/keys

# PUT /records/record/keys/key


# [ Update ]
#
# PATCH /records/record/keys/key


# [ Delete ]
#
# DELETE /records/record/keys/key


# [ Describe ]
#
# HEAD/INFO?


# iofun testing box
iofun = []

# e_tag
e_tag = False

class IndexHandler(web.RequestHandler):
    '''
        HTML5 Index
    '''
    def get(self):
        self.render('index.html', test="Hello, world!")

@gen.engine
def periodic_records_callbacks(stuff='bananas'):
    '''
        Mango periodic records
    '''
    assigned_false = yield motor.Op(periodic.process_assigned_false, db)
    asterisk_record = yield motor.Op(periodic.process_asterisk_cdr, db)

    for record in assigned_false:
        flag = yield motor.Op(
            periodic.assign_call,
            db,
            record['account'],
            record['id']
        )
        resource = yield motor.Op(periodic.new_resource_context, db, record)

    for record in asterisk_record:
        flag = yield motor.Op(
            periodic.assign_call,
            db,
            record['account'],
            record['id']
        )
        resource = yield motor.Op(periodic.new_resource_context, db, record)



if __name__ == '__main__':
    '''
        Manage Asynchronous Number Granular/Going ORGs

        Organizations of restricted generality
    '''
    opts = options.options()
    
    # Mango periodic functions
    periodic_records = opts.periodic_records
    
    # Set document database
    document = motor.MotorClient().open_sync().mango

    # Set default database
    db = document

    if opts.ensure_indexes:
        logging.info('Ensuring indexes...')
        indexes.ensure_indexes(db)
        logging.info('DONE.')
    
    # base url
    base_url = opts.base_url
    
    # mango application daemon
    application = web.Application(

        [
            (r'/', IndexHandler),

            (r'/jc/?', HomeHandler),

            # Tornado static file handler 
            (r'/static/(.*)', web.StaticFileHandler, {'path': './static'},),

            # basic-auth session
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),

            # users records 
            (r'/users/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/users/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            # users billing routes
            (r'/users/(?P<account>.+)/routes/?', accounts.RoutesHandler),

            # users
            (r'/users/?', accounts.UsersHandler),
            (r'/users/(?P<account>.+)/?', accounts.UsersHandler),

            # orgs records
            (r'/orgs/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/orgs/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            (r'/orgs/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/orgs/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            # orgs teams
            # (r'/orgs/(?P<account>.+)/teams/?', accounts.TeamsHandler),
            # (r'/orgs/(?P<account>.+)/teams/page/(?P<page_num>\d+)/?', accounts.TeamsHandler),
            # (r'/orgs/(?P<account>.+)/teams/(?P<team_id>.+)/?', accounts.TeamsHandler),

            # organizations of restricted generality
            (r'/orgs/?', accounts.OrgsHandler),
            (r'/orgs/(?P<account>.+)/?', accounts.OrgsHandler),

            # records
            (r'/records/start/(?P<start>.*)/stop/(?P<stop>.*)/?', records.Handler),
            (r'/records/start/(?P<start>.*)/?', records.Handler),
            (r'/records/stop/(?P<stop>.*)/?', records.Handler),
            (r'/records/page/(?P<page_num>\d+)/?', records.Handler),

            # public records 
            (r'/records/public/?', records.PublicHandler),
            (r'/records/public/page/(?P<page_num>\d+)/?', records.PublicHandler),

            # unassigned records
            (r'/records/unassigned/?', records.UnassignedHandler),
            (r'/records/unassigned/page/(?P<page_num>\d+)/?', records.UnassignedHandler),

            # records summary
            # (r'/records/summary/<lapse>/<value>/?', records.SummaryHandler),

            # return last (n) of lapse
            # (r'/records/summary/<lapse>/lasts/(?P<int>\d+)/?', records.SummaryHandler),

            # statistical projection based on the previous data.
            # (r'/records/summary/<lapse>/nexts/(?P<int>\d+)/?', records.SummaryHandler),

            # records summary
            (r'/records/summary/start/(?P<start>.*)/stop/(?P<stop>.*)/?', records.SummaryHandler),
            (r'/records/summary/start/(?P<start>.*)/?', records.SummaryHandler),
            (r'/records/summary/stopt/(?P<stop>.*)/?', records.SummaryHandler),

            (r'/records/summary/(?P<lapse>.*)/start/(?P<start>.*)/stop/(?P<stop>.*)/?', records.SummaryHandler),
            (r'/records/summary/(?P<lapse>.*)/start/(?P<start>.*)/?', records.SummaryHandler),
            (r'/records/summary/(?P<lapse>.*)/stop/(?P<stop>.*)/?', records.SummaryHandler),

            # return last (n) of lapse
            # (r'/records/summary/(?P<lapse>.*)/lasts/(?P<int>\d+)/?', records.SummaryHandler),

            (r'/records/summary/(?P<lapse>.*)/?', records.SummaryHandler),
            (r'/records/summary/?', records.SummaryHandler),

            # records summaries
            (r'/records/summaries/start/(?P<start>.*)/stop/(?P<stop>.*)/?', records.SummariesHandler),
            (r'/records/summaries/start/(?P<start>.*)/?', records.SummariesHandler),
            (r'/records/summaries/stop/(?P<stop>.*)/?', records.SummariesHandler),

            (r'/records/summaries/(?P<lapse>.*)/start/(?P<start>.*)/stop/(?P<stop>.*)/?', records.SummariesHandler),
            (r'/records/summaries/(?P<lapse>.*)/start/(?P<start>.*)/?', records.SummariesHandler),
            (r'/records/summaries/(?P<lapse>.*)/stop/(?P<stop>.*)/?', records.SummariesHandler),

            (r'/records/summaries/(?P<lapse>.*)/?', records.SummariesHandler),
            (r'/records/summaries/?', records.SummariesHandler),

            (r'/records/(?P<record_uuid>.+)/?', records.Handler),
            (r'/records/?', records.Handler),

            # This is a ugly hack: billings.RecordsHandler, the correct stuff: billings.Handler.
            # hmm, really?

            (r'/billings/(?P<billing_uuid>.+)/?', billings.RecordsHandler),
            (r'/billings/?', billings.RecordsHandler),

            (r'/billings/records/start/(?P<start>.*)/stop/(?P<stop>.*)/?', billings.RecordsHandler),
            (r'/billings/records/start/(?P<start>.*)/?', billings.RecordsHandler),
            (r'/billings/records/stop/(?P<stop>.*)/?', billings.RecordsHandler),
            (r'/billings/records/?', billings.RecordsHandler)

        ],

        # system database
        db=db,

        # periodic records
        periodic_records=periodic_records,

        # application timezone
        tz=pytz.timezone(opts.timezone),

        # pagination page size
        page_size=opts.page_size,

        # cookie settings
        cookie_secret=opts.cookie_secret,

        # static files (this is all the html, css, js and stuff)
        # on production environment the static stuff is served with nginx.

        static_path=os.path.join(os.path.dirname(__file__), "static"),

        template_path=os.path.join(os.path.dirname(__file__), "templates"),

        # login url
        login_url='/login'
    )

    # Set relational database
    application.sql = momoko.Pool(
        dsn='dbname=asterisk user=postgres',
        size=1
    )

    # Tornado periodic callbacks
    periodic_records = ioloop.PeriodicCallback(periodic_records_callbacks, 10000)
    periodic_records.start()

    # Setting up mango server processor
    application.listen(opts.port)
    logging.info('Listening on http://%s:%s' % (opts.host, opts.port))
    ioloop.IOLoop.instance().start()