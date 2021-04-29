#!/usr/bin/env python3

# This file is part of mango.


__author__ = "Jean Chassoul"


import logging
import uuid

import riak
from tornado import ioloop, web

from mango.handlers import accounts, tasks, teams
from mango.tools import options


def main():
    """
    mango main function
    """
    # mango daemon options
    opts = options.options()
    # Riak key-value storage
    kvalue = riak.RiakClient(host=opts.riak_host, pb_port=8087)
    # Our current db
    db = kvalue
    # Our system uuid
    system_uuid = uuid.uuid4()
    # logging system spawned
    logging.info("Mango system {0} spawned".format(system_uuid))
    # logging riak settings
    logging.info("Riak server: {0}:{1}".format(opts.riak_host, opts.riak_port))
    # streaming daemonic setup
    logging.info(
        "Streams spawn at: {0}:{1}".format(opts.spaceboard_host, opts.spaceboard_port)
    )
    # application web daemon
    application = web.Application(
        [
            # ORGs teams handler
            (r"/orgs/(?P<org_uuid>.+)/teams/page/(?P<page_num>\d+)/?", teams.Handler),
            (r"/orgs/(?P<org_uuid>.+)/teams/(?P<team_uuid>.+)/?", teams.Handler),
            (r"/orgs/(?P<org_uuid>.+)/teams/?", teams.Handler),
            # (Organizations of Restricted Generality) inspired at least!
            (r"/orgs/page/(?P<page_num>\d+)/?", accounts.OrgsHandler),
            (r"/orgs/(?P<org_uuid>.+)/?", accounts.OrgsHandler),
            (r"/orgs/?", accounts.OrgsHandler),
            # Simple user accounts
            (r"/users/page/(?P<page_num>\d+)/?", accounts.UsersHandler),
            (r"/users/(?P<user_uuid>.+)/?", accounts.UsersHandler),
            (r"/users/?", accounts.UsersHandler),
            # Tasks for humans and non-humans alike!
            (r"/tasks/page/(?P<page_num>\d+)/?", tasks.Handler),
            (r"/tasks/(?P<task_uuid>.+)/?", tasks.Handler),
            (r"/tasks/?", tasks.Handler),
        ],
        db=db,
        kvalue=kvalue,
        debug=opts.debug,
        domain=opts.domain,
        page_size=opts.page_size,
    )
    # Setting up the application server process
    application.listen(opts.port)
    logging.info("Listening on http://{0}:{1}".format(opts.host, opts.port))
    ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
