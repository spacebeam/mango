# -*- coding: utf-8 -*-
'''
    Mango client logic
'''

# This file is part of overlord.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import logging
import zmq

from tornado import gen

from zmq.eventloop.future import Context, Poller


@gen.coroutine
def publisher(port=8899):
    '''
        Please make the publisher the client (connect)

        heartbeat from publisher (the client) every X seconds
    '''
    context = Context()
    pub = context.socket(zmq.PUB)
    pub.connect("tcp://localhost:%s" % port)

    poller = Poller()
    poller.register(pub, zmq.POLLOUT)

    while True:
        topic = 'heartbeat'
        data = 'heartbeat'
        message = '{0} {1}'.format(topic, data)
        yield pub.send(message)
        yield gen.sleep(1)