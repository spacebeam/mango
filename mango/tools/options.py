# This file is part of mango.

# Distributed under the terms of the last AGPL License.


__author__ = 'Jean Chassoul'


import os
import tornado.options
from tornado.options import parse_config_file


config_path = 'mango.conf'


def options():
    '''
        Mango configuration options
    '''
    # set config stuff
    tornado.options.define(
        'config',
        type=str, help='path to config file',
        callback=lambda path: parse_config_file(path, final=False))
    # debugging
    tornado.options.define(
        'debug',
        default=False, type=bool,
        help=('Turn on autoreload and log to stderr only'))
    # logging dir
    tornado.options.define(
        'logdir',
        type=str, default='log',
        help=('Location of logging (if debug mode is off)'))
    # resource domain
    tornado.options.define(
        'domain',
        default='*', type=str,
        help='Application domain, e.g: "example.com"')
    # Server host
    tornado.options.define(
        'host',
        default='127.0.0.1', type=str,
        help=('Server hostname'))
    # Server port
    tornado.options.define(
        'port',
        default=8888, type=int,
        help=('Server port'))
    # Spaceboard hostname
    tornado.options.define(
        'spaceboard_host',
        default='127.0.0.1', type=str,
        help=('Streaming service hostname or ip address'))
    # Spaceboard port
    tornado.options.define(
        'spaceboard_port',
        default=8899, type=int,
        help=('Streaming port'))
    # Riak kvalue host
    tornado.options.define(
        'riak_host',
        default='127.0.0.1', type=str,
        help=('Riak cluster node'))
    # Riak kvalue port
    tornado.options.define(
        'riak_port',
        default=8087, type=int,
        help=('Riak cluster port'))
    # Page size
    tornado.options.define(
        'page_size',
        default=100, type=int,
        help=('Set a custom page size'))
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
