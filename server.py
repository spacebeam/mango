# -*- coding: utf-8 -*-
'''
    Manage Asynchronous Number General ORGs
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__authors__ = 'Team Machine'


import sys
import time
import uuid
import itertools
import logging
import riak
import motor
import queries
import pylibmc as mc
from tornado import gen
from tornado import web
from mango.tools import options, new_resource
from mango.handlers import LoginHandler, LogoutHandler
from mango.handlers import accounts
from mango.handlers import tasks
from zmq.eventloop import ioloop


# ioloop
ioloop.install()

# e_tag
e_tag = False
# standard db
db = False
# sql flag
sql = False


def main():
    '''
        Manage Asynchronous Number General ORGs

        Organizations of Restricted Generality.
    '''
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
    # key-value
    kvalue=False
    # memcached
    cache = memcache
    # sql
    global sql
    sql = queries.TornadoSession(uri=postgresql_uri)
    # current db
    global db
    db = document
    # system uuid
    system_uuid = uuid.uuid4()
    # logging system spawned uuid
    logging.info('Mango system uuid {0} spawned'.format(system_uuid))
    # logging database hosts
    logging.info('MongoDB server: {0}:{1}'.format(opts.mongo_host, opts.mongo_port))
    logging.info('PostgreSQL server: {0}:{1}'.format(opts.sql_host, opts.sql_port))
    # system cache
    cache_enabled = opts.cache_enabled
    if cache_enabled:
        logging.info('Memcached server: {0}:{1}'.format(opts.memcached_host, opts.memcached_port))
    # mango web application daemon
    application = web.Application(
        [
            # Mango Basic-Auth session
            (r'/login/?', LoginHandler),
            (r'/logout/?', LogoutHandler),
    
            # ORGs teams
            #(r'/orgs/(?P<account>.+)/teams/page/(?P<page_num>\d+)/?', accounts.TeamsHandler),
            #(r'/orgs/(?P<account>.+)/teams/(?P<team_uuid>.+)/?', accounts.TeamsHandler),
            #(r'/orgs/(?P<account>.+)/teams/?', accounts.TeamsHandler),
    
            # ORGs members
            #(r'/orgs/(?P<account>.+)/members/page/(?P<page_num>\d+)/?', accounts.MembersHandler),
            #(r'/orgs/(?P<account>.+)/members/(?P<user>.+)/?', accounts.MembersHandler),
            #(r'/orgs/(?P<account>.+)/members/?', accounts.MembersHandler),
            
            # Organizations of Random Generality.
            (r'/orgs/?', accounts.OrgsHandler),
            (r'/orgs/(?P<account>.+)/?', accounts.OrgsHandler),

            # Users suspended
            #(r'/users/suspended/?', accounts.UsersSuspendedHandler),
            
            # Users disable
            #(r'/users/disable/?', accounts.UsersDisableHandler),
    
            # Users active
            #(r'/users/active/?', accounts.UsersActiveHandler),
            
            # Users resources
            (r'/users/?', accounts.UsersHandler),
            (r'/users/(?P<account>.+)/?', accounts.UsersHandler),
            
            # Tasks now 
            (r'/tasks/now/?', tasks.NowHandler),
            
            # Tasks later 
            (r'/tasks/later/?', tasks.LaterHandler),
            
            # Tasks done
            (r'/tasks/done/?', tasks.DoneHandler),
            (r'/tasks/page/(?P<page_num>\d+)/?', tasks.Handler),
            
            # Tasks
            (r'/tasks/(?P<task_uuid>.+)/?', tasks.Handler),
            (r'/tasks/?', tasks.Handler),
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
        # pagination page size
        page_size=opts.page_size,
        # cookie settings
        cookie_secret=opts.cookie_secret,
        # login url
        login_url='/login/'
    )
    # Setting up mango
    application.listen(opts.port)
    logging.info('System %s Listening on http://%s:%s' % (system_uuid, opts.host, opts.port))
    loop = ioloop.IOLoop.instance()
    loop.start()

if __name__ == '__main__':
    main()