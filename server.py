# -*- coding: utf-8 -*-
'''
    Manage Asynchronous Number General ORGs

    Organizations of Roman Generality (ORGs)
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import time
import zmq
import sys
import uuid
import itertools

import logging

import motor
import queries
import pylibmc as mc

# system periodic cast callback
from tornado.ioloop import PeriodicCallback as PeriodicCast

from tornado import gen
from tornado import web

# from tornado import websocket

from mango.system import records as record_tools
from mango.system import server_push
from mango.system import server_pub
from mango.system import server_router

from mango.system import client

from mango.system import worker_task
from mango.system import client_task

from mango.tools import options
from mango.tools import indexes
from mango.tools import periodic

from mango.tools import new_resource

from mango.handlers import MangoHandler, LoginHandler, LogoutHandler

from mango.handlers import accounts
from mango.handlers import billings
from mango.handlers import tasks
from mango.handlers import records

from multiprocessing import Process

from zmq.eventloop import ioloop


NBR_CLIENTS = 10
NBR_WORKERS = 3

# ioloop
ioloop.install()

# iofun testing box
iofun = []

# e_tag
e_tag = False

# db global variable
db = False

# sql global variable
sql = False

# cache glogbal variable
cache = False


@gen.coroutine
def periodic_get_records():
    '''
        periodic_get_records callback function
    '''
    start = time.time()
    recs = record_tools.Records()
    raw_records = yield [
        #periodic.get_raw_records(sql, 888),
        periodic.get_query_records(sql, 1000),

        #periodic.process_assigned_false(db),
        #periodic.process_assigned_records(db),
    ]
    
    if all(record is None for record in raw_records):
        results = None
    else:
        results = list(itertools.chain.from_iterable(raw_records))

        for stuff in results:

            record = yield recs.new_detail_record(stuff, db)

            checked = yield periodic.checked_flag(sql, record.get('uniqueid'))

            #flag = yield periodic.assign_record(
            #    db,
            #    stuff.get('account'),
            #    stuff.get('uuid')
            #)

            # check new resource
            #resource = yield new_resource(db, stuff, 'records')
            # check this stuff up

    end = time.time()
    periodic_take = (end - start)

    logging.info('it takes {0} processing periodic {1}'.format(
        periodic_take,
        'callbacks for records resource.'
    ))


def main():
    '''
        Manage Asynchronous Number General ORGs

        Organizations of Roman Generality.
    '''
    # Now we can run a few servers and processes

    # Server daemons and ports
    server_push_port = "5556"
    server_pub_port = "5558"

    # System frontend & backend routers and ports
    frontend_port = "4144"
    backend_port = "4188"

    # Servers
    Process(target=server_push, args=(server_push_port,)).start()
    Process(target=server_pub, args=(server_pub_port,)).start()
    Process(target=server_router, args=(frontend_port,backend_port,)).start()

    # Clients
    Process(target=client, args=(server_push_port,server_pub_port,)).start()

    # Start background tasks
    def start(task, *args):
        process = Process(target=task, args=args)
        process.daemon = True
        process.start()
    for i in range(NBR_CLIENTS):
        start(client_task, i)
    for i in range(NBR_WORKERS):
        start(worker_task, i)

    # Initialize main loop state
    count = NBR_CLIENTS
    
    # daemon options
    opts = options.options()

    # Set document database
    document = motor.MotorClient(opts.mongo_host, opts.mongo_port).mango

    # Set memcached backend
    memcache = mc.Client(
        [opts.memcached_host],
        binary=opts.memcached_binary,
        behaviors={
            "tcp_nodelay": opts.memcached_tcp_nodelay,
            "ketama": opts.memcached_ketama
        }
    )

    # Set SQL URI
    postgresql_uri = queries.uri(
        host=opts.sql_host,
        port=opts.sql_port,
        dbname=opts.sql_database,
        user=opts.sql_user,
        password=None
    )

    # Set kvalue database
    kvalue = False

    # Set default cache
    global cache
    cache = memcache

    # Set SQL session
    global sql
    sql = queries.TornadoSession(uri=postgresql_uri)

    # Set default database
    global db
    db = document

    # logging database hosts
    logging.info('MongoDB server: {0}:{1}'.format(opts.mongo_host, opts.mongo_port))
    logging.info('PostgreSQL server: {0}:{1}'.format(opts.sql_host, opts.sql_port))

    # Ensure 
    if opts.ensure_indexes:
        logging.info('Ensuring indexes...')
        indexes.ensure_indexes(db)
        logging.info('DONE.')

    # base url
    base_url = opts.base_url

    # system cache
    cache_enabled = opts.cache_enabled

    if cache_enabled:
        logging.info('Memcached server: {0}:{1}'.format(opts.memcached_host, opts.memcached_port))

    # mango web application daemon
    application = web.Application(

        [
            # Mango system knowledge (quotes) and realtime events.
            (r'/system/?', MangoHandler),

            # Basic-Auth session
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),

            # ORGs records
            (r'/orgs/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/orgs/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            (r'/orgs/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/orgs/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            # ORGs teams
            (r'/orgs/(?P<account>.+)/teams/page/(?P<page_num>\d+)/?', accounts.TeamsHandler),
            (r'/orgs/(?P<account>.+)/teams/(?P<team_uuid>.+)/?', accounts.TeamsHandler),
            (r'/orgs/(?P<account>.+)/teams/?', accounts.TeamsHandler),

            # ORGs members
            (r'/orgs/(?P<account>.+)/members/page/(?P<page_num>\d+)/?', accounts.MembersHandler),
            (r'/orgs/(?P<account>.+)/members/(?P<user>.+)/?', accounts.MembersHandler),
            (r'/orgs/(?P<account>.+)/members/?', accounts.MembersHandler),

            # Organizations of Random Generality.
            (r'/orgs/?', accounts.OrgsHandler),
            (r'/orgs/(?P<account>.+)/?', accounts.OrgsHandler),

            # Users records 
            (r'/users/(?P<account>.+)/records/?', accounts.RecordsHandler),
            (r'/users/(?P<account>.+)/records/page/(?P<page_num>\d+)/?', accounts.RecordsHandler),

            # Users billing routes
            (r'/users/(?P<account>.+)/routes/?', accounts.RoutesHandler),

            # Users
            (r'/users/?', accounts.UsersHandler),
            (r'/users/(?P<account>.+)/?', accounts.UsersHandler),

            # Records
            (r'/records/start/(?P<start>.*)/end/(?P<end>.*)/?', records.Handler),
            (r'/records/start/(?P<start>.*)/?', records.Handler),
            (r'/records/end/(?P<end>.*)/?', records.Handler),
            (r'/records/page/(?P<page_num>\d+)/?', records.Handler),

            # Public records 
            (r'/records/public/?', records.PublicHandler),
            (r'/records/public/page/(?P<page_num>\d+)/?', records.PublicHandler),

            # Unassigned records
            (r'/records/unassigned/?', records.UnassignedHandler),
            (r'/records/unassigned/page/(?P<page_num>\d+)/?', records.UnassignedHandler),

            # Records summary
            # (r'/records/summary/<lapse>/<value>/?', records.SummaryHandler),

            # Return last (n) of lapse
            # (r'/records/summary/<lapse>/lasts/(?P<int>\d+)/?', records.SummaryHandler),

            # Statistical projection based on the previous data.
            # (r'/records/summary/<lapse>/nexts/(?P<int>\d+)/?', records.SummaryHandler),

            # Records summary
            (r'/records/summary/start/(?P<start>.*)/end/(?P<end>.*)/?', records.SummaryHandler),
            
            (r'/records/summary/start/(?P<start>.*)/?', records.SummaryHandler),
            
            (r'/records/summary/end/(?P<end>.*)/?', records.SummaryHandler),

            (r'/records/summary/(?P<lapse>.*)/start/(?P<start>.*)/end/(?P<end>.*)/?', records.SummaryHandler),
            (r'/records/summary/(?P<lapse>.*)/start/(?P<start>.*)/?', records.SummaryHandler),
            (r'/records/summary/(?P<lapse>.*)/end/(?P<end>.*)/?', records.SummaryHandler),

            # Return last (n) of lapse
            # (r'/records/summary/(?P<lapse>.*)/lasts/(?P<int>\d+)/?', records.SummaryHandler),

            (r'/records/summary/(?P<lapse>.*)/?', records.SummaryHandler),
            (r'/records/summary/?', records.SummaryHandler),

            # Records summaries
            (r'/records/summaries/start/(?P<start>.*)/end/(?P<end>.*)/?', records.SummariesHandler),
            (r'/records/summaries/start/(?P<start>.*)/?', records.SummariesHandler),
            (r'/records/summaries/end/(?P<end>.*)/?', records.SummariesHandler),

            (r'/records/summaries/(?P<lapse>.*)/start/(?P<start>.*)/end/(?P<end>.*)/?', records.SummariesHandler),
            (r'/records/summaries/(?P<lapse>.*)/start/(?P<start>.*)/?', records.SummariesHandler),
            (r'/records/summaries/(?P<lapse>.*)/end/(?P<end>.*)/?', records.SummariesHandler),

            (r'/records/summaries/(?P<lapse>.*)/?', records.SummariesHandler),
            (r'/records/summaries/?', records.SummariesHandler),

            # Records
            (r'/records/(?P<record_uuid>.+)/?', records.Handler),
            (r'/records/?', records.Handler),

            # Records
            (r'/tasks/(?P<task_uuid>.+)/?', tasks.Handler),
            (r'/tasks/?', tasks.Handler),

            # Billings
            (r'/billings/(?P<billing_uuid>.+)/?', billings.RecordsHandler),
            (r'/billings/?', billings.RecordsHandler),

            # Billings records
            (r'/billings/records/start/(?P<start>.*)/end/(?P<end>.*)/?', billings.RecordsHandler),
            (r'/billings/records/start/(?P<start>.*)/?', billings.RecordsHandler),
            (r'/billings/records/end/(?P<end>.*)/?', billings.RecordsHandler),
            (r'/billings/records/?', billings.RecordsHandler)
        ],

        # system database
        db=db,

        # system cache
        cache=cache,

        # cache enabled flag
        cache_enabled=cache_enabled,

        # document datastorage
        document=document,

        # kvalue datastorage
        kvalue=kvalue,

        # sql datastorage
        sql=sql,

        # debug mode
        debug=opts.debug,

        # application domain
        domain=opts.domain,

        # application timezone
        timezone=opts.timezone,

        # pagination page size
        page_size=opts.page_size,

        # cookie settings
        cookie_secret=opts.cookie_secret,

        # login url
        login_url='/login/'
    )

    # Mango periodic cast callbacks
    periodic_records = PeriodicCast(periodic_get_records, 5000)
    periodic_records.start()

    # Setting up mango processor
    application.listen(opts.port)
    logging.info('Listening on http://%s:%s' % (opts.host, opts.port))
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()