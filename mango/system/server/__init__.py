# -*- coding: utf-8 -*-
'''
    Mango server logic
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
def subscriber(port=8899):
    '''
        Please make the subscriber the server (bind)

        don't forget to make sure subscriber (the server) subscribe to the heartbeat. 

        If you do it that way reconnection will happen automatically
    '''
    logging.warning("Running SUB server process on port: {0}".format(port))
    context = Context()
    sub = context.socket(zmq.SUB)
    sub.bind("tcp://*:%s" % port)
    sub.setsockopt(zmq.SUBSCRIBE, "heartbeat")
    sub.setsockopt(zmq.SUBSCRIBE, "asterisk")
    sub.setsockopt(zmq.SUBSCRIBE, "logging")
    
    poller = Poller()
    poller.register(sub, zmq.POLLIN)
    while True:
        events = yield poller.poll(timeout=500)
        if sub in dict(events):
            msg = yield sub.recv()
            logging.info(msg)
        else:
            pass
            #logging.info('nothing to recv')
