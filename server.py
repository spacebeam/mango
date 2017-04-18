# -*- coding: utf-8 -*-
'''
    Manage Asynchronous Number General ORGs
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__authors__ = 'Team Machine'

# Check out our research, services and resources at the https://nonsense.ws laboratory.

__ooo__ = '''
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░╔░Ñß╠░░░░░░░░░░░░░░░░░░░░░░░»░░░░░░░░░░░░░░░░░░░░░
    ░░µ▄▄▄»░╔▄░░▄▄▄▄▄▄▄▄░░░ú░░░░░░░╔φm╫▒░╔▄░░▄░░▄╔░»▄▄»░░░░░µ░░▄▄▄▄▄▄▄▄▄▄▄▄░░▄░░▄H░░
    ░░║██▀░░░¼░░██████████▄x░]░µúµ╙▀▓▓▓░░░░░░╠░░╢▓╠░╠░¡µ»╗╩Ü░░▄█████████▀▀╫░░░░░╙▌░░
    ░░║░»╩░░░░░░░██████░░╙╠▀▄░░░╟╫╬Ñ▓▓▓░░╟░░░░░»░▓▓╫▓╫▌░µ▄▄╦╨▀▀╠░║█████░░░Ü░░░Üµ░»░░
    »░║▌h░░░░╠░░░███▄╙▀░Ñ╔░░Ü▀▓▓▓╫╫╫▓╫╫▌░µ░░░╟╔▄▓╫╫▓╫╫▓▓▓▀U░½µK╜ñ╙▀Ü»╨║█ñµ]░░░M░░µ░░
    ░░║█░╠▄░░▄▄░║███▀░░░░░»░╦░╔▓╫╫▓▓▓╫╫╫░▄╫░µ╙╫╫▓╫╫▓▓▓╫╫▓N▄Å░░░░░µ╩██▄██░▄▄▌░▓█▄▄▌░░
    ░░║█████╔██████▓▄░«░╦░░░░╙▓╫╫╫▓▓╫╫╫╫▓╫▓▌µñU╬╫▓╫╫╫▓╫╫▓▀░░░µ»m╠░║█████████░████▌░░
    h░║███████████████▄▄▄▄╬▓▌░╥▀╣▓╫╫╫╫╫»Ñ╠▀▓╬▓▓╫▓░╙▀╩╬▓▓╬▓▓╫░╠»U▄▄███████████████▌░░
    ░░║███████████████╫▓▓▓╫╫▓╫╬▓▀░hU╠Å▀░ñ╟╫╫M╠▀▀▀H«U╔░µ░╙╫╫╫▓▓╫╫╫╫███████████████▌░░
    »░║████╫██████████╫▓╫▓▓▓▓╫▌░░m░»»░░µ╙▀▓╫▓╩U▄φ░░░░╚░ñ░▄╫╫╫╫▓▓╫╫▓╫╫██████╫╫████▌░░
    ░░║█╫╫█▓╫█▓╫██╫▓╫╫▓▓▓╫▓╫╫╫╫▓░░░░µ≈Ü░░▄╣▓▓╫▓╫▓░Hµ░░░░╙╫╫╫▓╫▓╫▓▓╫▓███╫╫╫▓▓▓╫▓╫╫▌░░
    »░░╫╫╫╫▓▓╫╫╫╫█▓▀▀╨║╫█▓▓▓▓▓Ü▄╬╬░╟░½░╫▓╫▓▓▓▓▓╫╫▌½░░╠░▓▓▓╦▓╫╫╫▓╫▌▀▀▓██▓╫╫╫▓▓▓▓╫╫▌░░
    ░░╟╫╫╫╫▓▓▓▓╫▀░░U░U║╩▀╠▓╫╫╫╫╫▓▓▓▄╦▓█╢╫╫▓▓▓▓▓╫▓▓╠▀╬▓N▓▓▓▓▓▓▓▀▀▀U░░╠░░╢╫╫▓▓▓╫╫▓▀U░░
    »░░║╫╫▓╫╫▓Ü░«µ░░»░░░╝▓╫╫╫▓╫▓▓▓▓▓╫▓▓╙╫╫█▓▓▓▓╫╫M⌂╠▄▓▓▓▓▓╫▓▓▓╫▓░░░░░╙h╠╫╫▓▓╫▓░░░░░░
    »░»╙╫╙╦╟╫╫▓N░»░░»»D░h╦╟╫▓▓╫╫╫▓╫░≈╠»░▀░µ╙╫▌░⌂Ü░░▀▓╫╫▓▓╫▓▓▓╫▌░≈░╦µ░░░░╠»╫╙▓▓▓▓░░░░
    ░»»╦▓╦ô░▓█▀░h╟N▄╠░>▄▓█▓▓╫╬╫▓╫╫▀ñ>Ü░»░U»░█»»╠░░░╠µ╙╢▓╫╫███▓▓▓▄░░/░ñ░▓▓▓▓▄█▀░░░▌░░
    ░░░╫╫╫▓▀▓N╫▄D▓╫▓╫╫╫╫████▓▓████▄░ñ░░»»H«╔▌░ñ╠░░h╟«░║██████████╫╫╫▓▓╦╫╫█▀░▓▓▓▓╫▌░░
    ░░╟▓▓░U░╟▓╫▓▓▓▓▓╫╫▓╫╫╫██████████▄▄░░Å░h██░░▄p░╔░h░█████████╫╫▓╫╫╫▓▓╫▓╠░░╟╫▓╝▓Ü░░
    ░░╟╫╫╫▓»░▀░µ║╫╫╫▓▓▓╫╫███████████░░░███▓█████▌µ███▓██████████╫▓▓▓╫▓▓╫╫▓╬░░╠µ░║▌░░
    »░╠▓▀░h░░░⌂»»╫▓╫▓╫╫▓█▓████████▀██▄░████████████▀▀▀██████████▓█▓▓╫▓▓▓░░Ü░░░H░░▓░░
    »░░U░µÜ░░░Ü»░║▓▓█▓▓██████████▌░░╠»░██████████░░░╚░║█▀▀████████╫▓▓██▓Ü»U░░░Å░ñ╟░░
    »h╠╫░»╩░░»░░░▓▓▓▓██████████▄░░░░╙>░░██████▀░µ░¥░░░░░║██████████████╫░ñ░⌂░µ▄░░▓░░
    »░╔╫▌╦▓▓░║▓╫▓╫╫▓███████████▀░H░░h░░ñ▀▀▒╜███▓⌐░░░░µ≥░>╔█████████╫╫▓╫▓▓▓╫▓░▓╫▓▓Ñ░░
    »░░▓╫╫╫╫░▓╫╫╫▓▓▓╫██████████▄░µÜ░░╠h▄▄▄]U███░>╓▄▄░h░╠██▀▀███████╫╫▓▓▓╫▓╫╫▓╫╫▓▓▓░░
    »h░▓▓█╫▓▓╫╫╫▓▓▓╫╫╫▓▀▀Ü░░║███████▄▄»▓███▀█▄▄░░║██████▄▒░░██▀▀╙╙╫╫╫╫▓▓▓▓╫╫▓╫╫▓▓▓░░
    »h░▓╫▓╫▓╟╫╫╫╫▓▓▓╫╫░╟≥░░░░░▄▓█████████░m░║█████████████▄░░░░░░╦░╙╩▓▓▓▓╫╫▌║╫╫╫▓▓░░
    »»░▓▀╩▓H░▀▀░▓▓▌╫╩▓╩░░»░µ«░▀▀███████████░░▀▀»║████████░░ñ░░░░░░░▄╗▓╫▓╙▀▀░░╠░░╣╫░░
    h░░Üñ░ó░░░Ü░╜╫»░µ▄▄»╗^░░U░╔█████████▀░╠░░░Ü░╙███████▀██▄░µ░]░µ▄╙▀▓▓░╙░Ñ░░░U»╨▓░░
    »░░░ññU░░░]≥░║▓╫╫╫╫░µ▄╦≡ñ▀▀░U░████▀▌≈░Ü░»░╠»»║█████▌░░░░X▄µ░░▓▓╫▓▓█U░µH░░░ù<░╬░░
    ░h╔▓░µ╠░░░Ü╦▓╫▓▓╫╫╫╫╫▀>⌂ñµÅ░░░╙╠░╫╔█░µ½░░µÜh>▓██▓▄»░░░Ñµ╩╙▀╬╫╫╫╫╫╫▓╫░≈Ñ░░╔▄▓╫▓░░
    »h░╫Mµ╬▓µ╝▀▓╫▓╫▓▓▓╫╫╫╫╦»░░░░░µ║██▄██▌▄██░╫██▓███▀µhU░░░░░Ü▄╫╫╫╫▓▓▓╫╫▄╦▓▓x╙▀╣▓╫░░
    hñ░╫╫▓▓▓▌φ╠╫▓╫╫╫╫▓╫╫▓▀▄▄«╔hU░░██████████▌████████▄░░╠ñ░»µµ▀▓╫╫╫╫╫╫╫▓▓▓╫▓M╩╠▓▓▓░░
    »░░▌╩╠Ü╠▓▓╫╫▓▌»╙▀▀▀█▓▓▓╫░╠▄╦╫╗█████████████████████╫╬▓▓▓╫@K╩╠▓╩╩▓▓╫▌╨░N║▓▓▓▓▓▌░░
    »░░░░▄▓▓▌╬╙╠▀▀»░╟░x░µ▀▓╫▓╫╫▓▓╫╫███████████████████╫╫▓▓╫╫▓▓╫▓▀░Ü░m^╙»░╬█▓▌╠Ü╠╙╙░░
    ░░░╔╙▀█╫╫╨▄╫╣░░░░░ñÜ╔╦▓▓▓▓▓▓▓╫▓▓╫███████▓██╫██████╫╫▓▓▓▓╫╫▓▄░ñ░░░░░╔╙╙▀▓╫╬▓▓╫K░░
    »»░░░▄╬╫▓╫╫╫╫░ñ%U░░░╙▀▓╫╫╫▓╫╫╫▓█████╫╫▓▓▓╫▓╫╫█╫█▓▓╫▓▓╫▓╫▓╫╫▓░;»╔»D░U╔╬▓▓▓▓▓▓╫░░░
    »░░╟▓╫▓▓▓▓▓▓▓▓▄▄░╟░█╫▓▓█▓▓▓▓▓▌╙▀▀▀██╫▓╫▓▓▓▓╫╫█▀░»░║╫╫▓▓╣▓▓▓Φ▓╫▌░m░▄╬╫▓▓▓▓▓▓▓╫▓░░
    »░░╟╫╫▓▓▓▓█▓╫╫╠Å╫╫N▓╫▓▓╫▓▓Ü╙╙░h░╠░U╙╫╫▓▓▓╫╫▓Ü░░½«░░╙»▄▓╫╫╫╫╫▓╫▓▓▓█╫▀╫▓╫╫▓▓▓╫▓▓░░
    »░░░▓╫▓▓▓╫╩▓╫▌U╠▄╬▓╫▓▓▓╫╫╫╫▓M░░░░░ñ»▓╫▓▀╫╫▓¿ñHÜ»░»░╔╙▀╫╫▓╫▓▓▓╫▓▓▀█▓░█╫▓▀╫╫▀▀▓Ü░░
    ░h░░╠░µ╙╫▓«µ░░░╠▀▓╫╫╫▓╫▓▓╫▓░░░ñ>⌂░░░»H╠Ü▓▓╫█▀»░µ>m╙░╔#▓╫╫╫▓╫▓╫╫░ñ╗░░╚«»^╟▌░ñÑ░░░
    hh░░░U»h█░h╗░░░╟%⌂▀▓╫▓▓██▓╫▓N▄▄╔░╠░╟█▓▓╦║▀╠Uµß╫▓N╦▄▓████▓▓╫▓▓▓▌µ░Ü░░»Kñ░╟░░░░░░░
    »░h░░H═╗▌░ñ╟░░░╟ñU╟██████████╫╫╫▓▓╦╫╫▓▀╦╝╫▓▓▓╫╫╫╫▓╫▓╫██████████▄░ì░░»Ü░╠█░µ░░░░░
    »»»░╠ññ██░░▄▄░╔▄░░█████████╫╫▓▓╫▓▓▓╫╫╦▒µm╢█╩▀╫╫╫╫╫╫╫╫╫███████████▀µ░▄▄░║█▌▄▄▓░░░
    »»░║████████▌░██████████████▓╫▓▓╫╫╫▓╫▓╨Ü░░U«░▓╫╫╫╫╫▓╫███████████▄Uµ║█████████░░░
    »h░██████████▄██▀▀╙█████████▓█▓╫╫╫▓▓▀µ╬░░░╟ñ^╙╫╫▓▓╫███████████╙▀▀▀K███████████░░
    »h░██████████▀░½░¼░█▀▀▄████████▓█▓██▒░╩░░░╟░░ñ█████████████▀▀▀░U╟░h╙█████████▀░░
    »h░░██████▀▀U░Nñ░░░░░██████████████╫▓h░▄░░▄▄░║▓▓████████████Kµ░░░░ñU███████░░«░░
    »░h½█▀░╜██▀K»Ü»░░░»╨h░»▀▀█▀█▀▀▀▀▀▀▀▀╩╩▀▀H»▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀»░╨hh░»»/╠░╚ñ║▀▀▀M░░░
    »»»╨╚╙╨░╙╙░╨"!╙░╙╚░╩^^╨^░"h░░""░Ü"░░░^╚"╚╨░»»░░░»░»»░░»»░░»░»»░»»»»»»»»»»░░░░░»» 
'''


import time
import uuid
import itertools
import logging
import riak
import motor
import queries
import pylibmc as mc
from tornado.ioloop import PeriodicCallback as Cast     # MISSING PERIODIC CAST
from tornado import gen, web
from mango.tools import options, new_resource           # MISSING NEW RESOURCE
from mango.handlers import LoginHandler, LogoutHandler
from mango.handlers import accounts, tasks
from zmq.eventloop import ioloop


# ioloop
ioloop.install()

# e_tag
e_tag = False

# WHY ARE THIS GLOBAL NONSENSE STILL HERE? FINISH MEASURE AND DELETE IT

# standard db
db = False
# sql flag
sql = False


def main():
    '''
        Organizations of Random Generality.
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
    # riak key-value storage
    kvalue = riak.RiakClient(host=opts.riak_host, pb_port=8087)
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
    # logging riak settings
    logging.info('Riak server: {0}:{1}'.format(opts.riak_host, opts.riak_port))
    # logging old database hosts
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
            (r'/orgs/(?P<account_uuid>.+)/?', accounts.OrgsHandler),

            # Users suspended
            #(r'/users/suspended/?', accounts.UsersSuspendedHandler),
            
            # Users disable
            #(r'/users/disable/?', accounts.UsersDisableHandler),
    
            # Users active
            #(r'/users/active/?', accounts.UsersActiveHandler),
            
            # Users resources
            (r'/users/?', accounts.UsersHandler),
            (r'/users/(?P<account>.+)/?', accounts.UsersHandler),
            (r'/users/(?P<account_uuid>.+)/?', accounts.UsersHandler),

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