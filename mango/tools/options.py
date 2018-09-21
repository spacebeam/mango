# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Space Beam LLC'


import os
import uuid
import tornado.options
from tornado.options import parse_config_file


config_path = 'mango.conf'


def options():
    '''
        Mango configuration options
    '''
    # set config stuff
    tornado.options.define('config',
        type=str, help='path to config file',
        callback=lambda path: parse_config_file(path, final=False))
    # debugging
    tornado.options.define('debug',
        default=False, type=bool,
        help=('Turn on autoreload and log to stderr only'))
    # logging dir
    tornado.options.define('logdir',
        type=str, default='log',
        help=('Location of logging (if debug mode is off)'))
    # resource domain
    tornado.options.define('domain',
        default='*', type=str,
        help='Application domain, e.g: "example.com"')
    # Solr hotname
    tornado.options.define('solr',
        default='nonsense.ws', type=str,
        help='Application solr, e.g: "example.com"')
    # server host
    tornado.options.define('host',
        default='127.0.0.1', type=str,
        help=('Server hostname'))
    # server port
    tornado.options.define('port',
        default=8888, type=int,
        help=('Server port'))
    # daemonic hostname
    tornado.options.define('daemons_host',
        default='127.0.0.1', type=str,
        help=('Daemonic service hostname or ip address'))
    # daemonic port
    tornado.options.define('daemons_port',
        default=8899, type=int,
        help=('Daemons port'))
    # Riak kvalue host
    tornado.options.define('riak_host',
        default='127.0.0.1', type=str,
        help=('Riak cluster node'))
    # Riak kvalue port
    tornado.options.define('riak_port',
        default=8087, type=int,
        help=('Riak cluster port'))
    # Kong admin host
    tornado.options.define('kong_host',
        default='127.0.0.1', type=str,
        help=('Kong Admin API'))
    # Kong admin port
    tornado.options.define('kong_port',
        default=8001, type=int,
        help=('Kong Admin API port'))
    # PostgreSQL database settings
    tornado.options.define('sql_host',
        type=str, help=('PostgreSQL hostname or ip address'))
    # SQL port
    tornado.options.define('sql_port',
        default=5432, type=int,
        help=('PostgreSQL port'))
    # SQL database
    tornado.options.define('sql_database',
        type=str, help=('PostgreSQL database'))
    # SQL user
    tornado.options.define('sql_user',
        type=str, help=('PostgreSQL username'))
    # SQL password
    tornado.options.define('sql_password',
        type=str, help=('PostgreSQL username password'))
    # memcache host
    tornado.options.define('memcached_host',
        default='127.0.0.1', type=str,
        help=('Memcached host'))
    # memcache port
    tornado.options.define('memcached_port',
        default=11211, type=int,
        help=('Memcached port'))
    tornado.options.define('memcached_binary',
        default=True, type=bool,
        help=('Memcached binary'))
    tornado.options.define('memcached_tcp_nodelay',
        default=True, type=bool,
        help=('Memcached tcp_nodelay'))
    tornado.options.define('memcached_ketama',
        default=True, type=bool,
        help=('Memcached ketama'))
    tornado.options.define('cache_enabled',
        default=False, type=bool,
        help=('Enable cache'))
    tornado.options.define('page_size',
        default=50, type=int,
        help=('Set a custom page size up to 50'))
    # Parse config file, then command line...
    # so command line switches take precedence
    if os.path.exists(config_path):
        print('Loading %s' % (config_path))
        tornado.options.parse_config_file(config_path)
    else:
        print('No config file at %s' % (config_path))
    tornado.options.parse_command_line()
    result = tornado.options.options
    for required in ('domain', 'host', 'port'):
        if not result[required]:
            raise Exception('%s required' % required)
    return result
