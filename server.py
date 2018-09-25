# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Space Beam LLC'


import uuid
import riak
import logging
import pylibmc as mc
from tornado import ioloop
from tornado.ioloop import PeriodicCallback as Cast
from tornado import gen, web
from mango.handlers import accounts, teams, tasks
from mango.tools import check_new_accounts, options


def main():
    '''
        mango main function
    '''
    # mango daemon options
    opts = options.options()
    # Set memcached backend
    memcache = mc.Client(
        [opts.memcached_host],
        binary=opts.memcached_binary,
        behaviors={
            "tcp_nodelay": opts.memcached_tcp_nodelay,
            "ketama": opts.memcached_ketama
        }
    )
    # Riak key-value storage
    kvalue = riak.RiakClient(host=opts.riak_host, pb_port=8087)
    # Cache memcached service
    cache = memcache
    # Our current db
    db = kvalue
    # Our system uuid
    system_uuid = uuid.uuid4()
    # Solr 4.7 Full-text search 
    solr = opts.solr
    # logging system spawned
    logging.info('Mango system {0} spawned'.format(system_uuid))
    # logging solr
    logging.info('Solr 4.7 https://{0}/search/'.format(solr))
    # logging riak settings
    logging.info('Riak server: {0}:{1}'.format(opts.riak_host, opts.riak_port))
    # check for cache
    cache_enabled = opts.cache_enabled
    if cache_enabled:
        logging.info('Memcached server: {0}:{1}'.format(opts.memcached_host, opts.memcached_port))
    # logging kong settings
    logging.info('Kong Admin API: {0}:{1}'.format(opts.kong_host, opts.kong_port))
    # logging current daemonic setup
    logging.ingo('Daemons spawn at: {0}:{1}'.format(opts.daemons_host, opts.daemons_port))
    # application web daemon
    application = web.Application(
        [
            # ORGs teams handler
            (r'/orgs/(?P<org_uuid>.+)/teams/page/(?P<page_num>\d+)/?', teams.Handler),
            (r'/orgs/(?P<org_uuid>.+)/teams/(?P<team_uuid>.+)/?', teams.Handler),
            (r'/orgs/(?P<org_uuid>.+)/teams/?', teams.Handler),
            # (Organizations of Restricted Generality)
            (r'/orgs/page/(?P<page_num>\d+)/?', accounts.OrgsHandler),
            (r'/orgs/(?P<org_uuid>.+)/?', accounts.OrgsHandler),
            (r'/orgs/?', accounts.OrgsHandler),
            # Simple user accounts
            (r'/users/page/(?P<page_num>\d+)/?', accounts.UsersHandler),
            (r'/users/(?P<user_uuid>.+)/?', accounts.UsersHandler),
            (r'/users/?', accounts.UsersHandler),
            # Tasks for humans and non-humans alike!
            (r'/tasks/page/(?P<page_num>\d+)/?', tasks.Handler),
            (r'/tasks/(?P<task_uuid>.+)/?', tasks.Handler),
            (r'/tasks/?', tasks.Handler),
        ],
        db = db,
        cache = cache,
        kvalue = kvalue,
        debug = opts.debug,
        domain = opts.domain,
        page_size = opts.page_size,
        solr = opts.solr,
    )
    # Periodic Cast Functions
    check_kong_consumers = Cast(check_new_accounts, 1000)
    check_kong_consumers.start()
    # Setting up the application server process
    application.listen(opts.port)
    logging.info('Listening on http://{0}:{1}'.format(opts.host, opts.port))
    ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
