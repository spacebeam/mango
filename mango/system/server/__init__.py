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

'''
@gen.coroutine
def subscriber(port=8899):

    # TODO: this is commented out because we're using a hack implementation on server.py, please fix it.

    logging.warning("Binding SUB socket on port: {0}".format(port))
    context = Context()
    sub = context.socket(zmq.SUB)
    sub.bind("tcp://*:%s" % port)

    sub.setsockopt(zmq.SUBSCRIBE, "heartbeat")
    sub.setsockopt(zmq.SUBSCRIBE, "asterisk")
    sub.setsockopt(zmq.SUBSCRIBE, "logging")
    sub.setsockopt(zmq.SUBSCRIBE, "upload")

    poller = Poller()
    poller.register(sub, zmq.POLLIN)
    while True:
        events = yield poller.poll(timeout=500)
        if sub in dict(events):
            #logging.info(msg)
            msg = yield sub.recv()
            if msg.startswith('heartbeat'):
                msg = msg.split(' ')[1]
                # websocket send
                wsSend({'message':msg})
            elif msg.startswith('asterisk'):
                msg = msg.split(' ')[1]
                # websocket send
                wsSend(msg)
            elif msg.startswith('logging'):
                pass
        else:
            #logging.info('nothing to recv')
            pass
'''