import zmq
import logging
import riak
import uuid
import pylibmc as mc
from tornado.web import RequestHandler
from tornado import gen, web
#from mango.handlers import LoginHandler, LogoutHandler
from mango.handlers import accounts, tasks, teams, orgs
from mango.tools import options
from zmq.eventloop import ioloop

# ioloop
ioloop.install()

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
    # riak key-value
    kvalue = riak.RiakClient(host=opts.riak_host, pb_port=8087)
    # memcached
    cache = memcache
    # current db
    db = kvalue
    # system uuid
    system_uuid = uuid.uuid4()
    # yokozuna solr
    solr = opts.solr
    # logging system spawned
    logging.info('Mango system {0} spawned'.format(system_uuid))
    # logging solr
    logging.info('Solr riak {0} '.format(solr))
    # logging riak settings
    logging.info('Riak server: {0}:{1}'.format(opts.riak_host, opts.riak_port))
    # check for cache
    cache_enabled = opts.cache_enabled
    if cache_enabled:
        logging.info('Memcached server: {0}:{1}'.format(opts.memcached_host, opts.memcached_port))
    # application web daemon
    application = web.Application(
        [
            # Mango Basic-Auth session
            #(r'/login/?', LoginHandler),
            #(r'/logout/?', LogoutHandler),
            # ORGs teams
            #(r'/orgs/(?P<account>.+)/teams/page/(?P<page_num>\d+)/?', accounts.TeamsHandler),
            #(r'/orgs/(?P<account>.+)/teams/(?P<team_uuid>.+)/?', accounts.TeamsHandler),
            #(r'/orgs/(?P<account>.+)/teams/?', accounts.TeamsHandler),
            # ORGs members
            #(r'/orgs/(?P<account>.+)/members/page/(?P<page_num>\d+)/?', accounts.MembersHandler),
            #(r'/orgs/(?P<account>.+)/members/(?P<user>.+)/?', accounts.MembersHandler),
            #(r'/orgs/(?P<account>.+)/members/?', accounts.MembersHandler),
            # Organizations of Random Generality.
            #(r'/orgs/?', orgs.OrgsHandler),
            #(r'/orgs/(?P<org>.+)/?', orgs.OrgsHandler),
            #(r'/orgs/(?P<org_uuid>.+)/?', orgs.OrgsHandler),
            # Users suspended
            #(r'/users/suspended/?', accounts.UsersSuspendedHandler),
            # Users disable
            #(r'/users/disable/?', accounts.UsersDisableHandler),
            # Users active
            #(r'/users/active/?', accounts.UsersActiveHandler),
            # Users resources
            #(r'/users/?', accounts.UsersHandler),
            #(r'/users/(?P<account>.+)/?', accounts.UsersHandler),
            #(r'/users/(?P<account_uuid>.+)/?', accounts.UsersHandler),
            # Tasks now 
            #(r'/tasks/now/?', tasks.NowHandler),
            # Tasks later 
            #(r'/tasks/later/?', tasks.LaterHandler),
            # Tasks done
            #(r'/tasks/done/?', tasks.DoneHandler),
            #(r'/tasks/page/(?P<page_num>\d+)/?', tasks.Handler),            
            #(r'/tasks/(?P<task_uuid>.+)/?', tasks.Handler),
            #(r'/tasks/?', tasks.Handler),

            (r'/users/page/(?P<page_num>\d+)/?', accounts.UsersHandler),
            (r'/users/(?P<account_uuid>.+)/?', accounts.UserHandler),
            (r'/users/?', accounts.UsersHandler),
            
            #(r'/orgs/page/(?P<page_num>\d+)/?', orgs.OrgsHandler),
            #(r'/orgs/(?P<org_uuid>.+)/?', orgs.OrgsHandler),
            #(r'/orgs/?', orgs.OrgsHandler),

            (r'/teams/page/(?P<page_num>\d+)/?', accounts.TeamsHandler),
            (r'/teams/(?P<team_uuid>.+)/?', accounts.Teamsandler),
            (r'/teams/?', accounts.TeamsHandler),
        ],
        db = db,
        cache = cache,
        kvalue = kvalue,
        debug = opts.debug,
        domain = opts.domain,
        page_size = opts.page_size,
        solr = opts.solr,
    )  
    # Setting up the application server process
    application.listen(opts.port)
    logging.info('Listening on http://{0}:{1}'.format(opts.host, opts.port))
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    '''
        Cas for monkey systems
    '''
    main()