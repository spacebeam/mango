# -*- coding: utf-8 -*-
'''
    Manage Asynchronous Number of Granular/Going ORGs
'''


# This file is part of mango.
#
# Distributed under the terms of the last AGPL License. The full
# license is in the file LICENCE, distributed as part of this
# software.


# BAD WOLF
# --------
# This is all about Wittgenstein
# real-time is all about kinetic movement
# this is all about Gabriel Naum
# listen to the realistic manifesto.

# More about what we mean with Organizations of Restricted Generality.
# http://www.exso.com/courses/cs101c/agents19/node3.html

# More on actor theory
# http://web.media.mit.edu/~lieber/Lieberary/OOP/Act-1/Concurrent-OOP-in-Act-1.html

# The maximum possible speed-up of a program as a result of parallelization is known as Amdahl's law. 
# - Wikipedia (I have to put a wikipedia quote here to make it funny.)

# The follow paper explains the foundations of our cloud system (or at least what we're trying to achieve).
# http://arxiv.org/pdf/0903.0694.pdf


__author__ = 'Jean Chassoul'

import os

from tornado import ioloop
from tornado import gen
from tornado import web

# from tornado import websocket

from mango.handlers import base
from mango.handlers import accounts
from mango.handlers import billings
from mango.handlers import records

from mango.tools import options
from mango.tools import indexes
from mango.tools import periodic

import logging

# cebus is the one who controls the goals it have a execute model build up on salt.
# for more on salt (https://medium.com/fun-technology/2a53b67b6903)

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

    for c in assigned_false:
      flag = yield motor.Op(periodic.assign_call, db, c['account'], c['id'])
      resource = yield motor.Op(periodic.new_resource_context, db, c)

    for c in asterisk_record:
      flag = yield motor.Op(periodic.assign_call, db, c['account'], c['id'])
      resource = yield motor.Op(periodic.new_resource_context, db, c)



if __name__ == '__main__':
    '''
        Manage Asynchronous Number Granular/Going ORGS
    '''
    opts = options.options()
    
    # Mango periodic functions
    periodic_records = opts.periodic_records
    
    # Set database back-end
    db = motor.MotorClient().open_sync().mango
    
    if opts.ensure_indexes:
        logging.info('Ensuring indexes...')
        indexes.ensure_indexes(db)
        logging.info('DONE.')
    
    # base url
    base_url = opts.base_url
    
    # mango application system daemon
    application = web.Application(

        [
            (r'/', IndexHandler),

            (r'/jc/?', base.HomeHandler),

            # Tornado static file handler 
            (r'/static/(.*)', web.StaticFileHandler, {'path': './static'},),

            # Mango basic-auth session
            (r'/login/?', base.MangoLoginHandler),
            (r'/logout/?', base.MangoLogoutHandler),

            # Mango users records 
            (r'/users/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/users/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            # Mango users billing routes
            (r'/users/(?P<account>.+)/routes/?', accounts.RoutesHandler),

            # Mango users
            (r'/users/?', accounts.UsersHandler),
            (r'/users/(?P<account>.+)/?', accounts.UsersHandler),

            # Mango ORG's records
            (r'/orgs/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/orgs/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            (r'/orgs/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/orgs/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            # Mango ORG's teams
            # (r'/orgs/(?P<account>.+)/teams/?', accounts.TeamsHandler),
            # (r'/orgs/(?P<account>.+)/teams/page/(?P<page_num>\d+)/?', accounts.TeamsHandler),
            # (r'/orgs/(?P<account>.+)/teams/(?P<team_id>.+)/?', accounts.TeamsHandler),

            # Mango ORG's
            (r'/orgs/?', accounts.OrgsHandler),
            (r'/orgs/(?P<account>.+)/?', accounts.OrgsHandler),

            # Mango records
            (r'/records/start/(?P<start>.*)/stop/(?P<stop>.*)/?', records.Handler),
            (r'/records/start/(?P<start>.*)/?', records.Handler),
            (r'/records/stop/(?P<stop>.*)/?', records.Handler),
            (r'/records/page/(?P<page_num>\d+)/?', records.Handler),

            # Mango public records 
            (r'/records/public/?', records.PublicHandler),
            (r'/records/public/page/(?P<page_num>\d+)/?', records.PublicHandler),

            # Mango unassigned records
            (r'/records/unassigned/?', records.UnassignedHandler),
            (r'/records/unassigned/page/(?P<page_num>\d+)/?', records.UnassignedHandler),

            # Mango records summary
            # (r'/records/summary/<lapse>/<value>/?', records.SummaryHandler),

            # Return last (n) of lapse
            # (r'/records/summary/<lapse>/lasts/(?P<int>\d+)/?', records.SummaryHandler),

            # Statistical projection based on the previous data.
            # (r'/records/summary/<lapse>/nexts/(?P<int>\d+)/?', records.SummaryHandler),

            # Mango records summary
            (r'/records/summary/start/(?P<start>.*)/stop/(?P<stop>.*)/?', records.SummaryHandler),
            (r'/records/summary/start/(?P<start>.*)/?', records.SummaryHandler),
            (r'/records/summary/stopt/(?P<stop>.*)/?', records.SummaryHandler),

            (r'/records/summary/(?P<lapse>.*)/start/(?P<start>.*)/stop/(?P<stop>.*)/?', records.SummaryHandler),
            (r'/records/summary/(?P<lapse>.*)/start/(?P<start>.*)/?', records.SummaryHandler),
            (r'/records/summary/(?P<lapse>.*)/stop/(?P<stop>.*)/?', records.SummaryHandler),

            # Return last (n) of lapse
            # (r'/records/summary/(?P<lapse>.*)/lasts/(?P<int>\d+)/?', records.SummaryHandler),

            (r'/records/summary/(?P<lapse>.*)/?', records.SummaryHandler),
            (r'/records/summary/?', records.SummaryHandler),

            # Mango records summaries
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

            # Campaigns ?

            # This is a ugly hack: billings.RecordsHandler, the correct stuff: billings.Handler.

            (r'/billings/(?P<billing_uuid>.+)/?', billings.RecordsHandler),
            (r'/billings/?', billings.RecordsHandler),

            (r'/billings/records/start/(?P<start>.*)/stop/(?P<stop>.*)/?', billings.RecordsHandler),
            (r'/billings/records/start/(?P<start>.*)/?', billings.RecordsHandler),
            (r'/billings/records/stop/(?P<stop>.*)/?', billings.RecordsHandler),
            (r'/billings/records/?', billings.RecordsHandler)

        ],
        
        # Mango api configuration
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
        
        # API login url
        login_url='/login'
    )
    
    application.sql = momoko.Pool(
        dsn='dbname=asterisk user=postgres host=127.0.0.1 password=',
        size=1
    )

    # Tornado periodic callbacks
    periodic_records = ioloop.PeriodicCallback(periodic_records_callbacks, 10000)
    periodic_records.start()

    # Setting up mango server processor
    application.listen(opts.port)
    logging.info('Listening on http://%s:%s' % (opts.host, opts.port))
    ioloop.IOLoop.instance().start()