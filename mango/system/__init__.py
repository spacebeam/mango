# -*- coding: utf-8 -*-
'''
    Mango system logic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import zmq

from zmq.eventloop import ioloop, zmqstream

import time
import random

import logging
import base64


def basic_authentication(handler_class):
    '''
        @basic_authentication

        HTTP Basic Authentication Decorator
    '''

    def wrap_execute(handler_execute):
        '''
            Wrap Execute basic authentication function
        '''

        def basic_auth(handler, kwargs):
            '''
                Basic AUTH implementation
            '''
            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Basic '):
                handler.set_status(403)
                handler.set_header('WWW-Authenticate', 'Basic '\
                                   'realm=mango') # get realm for somewhere else.
                handler._transforms = []
                handler.finish()
                return False
            auth_decoded = base64.decodestring(auth_header[6:])
            handler.username, handler.password = auth_decoded.split(':', 2)
            logging.info('Somewhere %s enter the dungeon! /api/ @basic_authentication' % handler.username)
            return True

        def _execute(self, transforms, *args, **kwargs):
            '''
                Execute the wrapped function
            '''
            if not basic_auth(self, kwargs):
                return False
            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)

    return handler_class

def get_command(message):
    '''
        get_command system function
    '''
    logging.warning('Received control command: {0}'.format(message))
    if message[0] == "Exit":
        logging.warning('Received exit command, client will stop receiving messages')
        should_continue = False
        ioloop.IOLoop.instance().stop()
        
def process_message(message):
    '''
        process_message system function
    '''
    logging.warning("Processing ... {0}".format(message))


def client_task(ident):
    """
        Basic request-reply client using REQ socket.
    """
    context = zmq.Context()
    socket_req = context.socket(zmq.REQ)
    socket_req.identity = u"Client-{}".format(ident).encode("ascii")
    socket_req.connect("tcp://localhost:%s" % '4144')
    stream_req = zmqstream.ZMQStream(socket_req)

    # Send request, get reply
    socket_req.send(b"HELLO")
    reply = socket_req.recv()
    logging.warning("{}: {}".format(socket_req.identity.decode("ascii"),
                          reply.decode("ascii")))

def worker_task(ident):
    """
        Worker task, using a REQ socket to do load-balancing.
    """
    context = zmq.Context()
    socket_req = context.socket(zmq.REQ)
    socket_req.identity = u"Worker-{}".format(ident).encode("ascii")
    socket_req.connect("tcp://localhost:%s" % '4188')
    stream_req = zmqstream.ZMQStream(socket_req)
    # Tell broker we're ready for work
    socket_req.send(b"READY")

    while True:
        address, empty, request = socket_req.recv_multipart()
        logging.warning("{}: {}".format(socket_req.identity.decode("ascii"),
                              request.decode("ascii")))
        socket_req.send_multipart([address, b"", b"OK"])


def gen_daemon(server_router):
    '''
        OTP gen_server analogy
    '''
    pass

def server_push(port="5556"):
    '''
        PUSH process
    '''
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:%s" % port)
    logging.warning("Running server on port: {0}".format(port))
    message = 'Continue'
    # serves only 5 request and dies
    while message == 'Continue':
        socket.send(message)
        time.sleep(1)
    socket.send("Exit")

def server_pub(port="5558"):
    '''
        PUB process
    '''
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    publisher_id = random.randrange(0,9999)
    logging.warning("Running PUB server process on port: {0}".format(port))

    while True:
        # Wait for next request from client
        topic = random.randrange(8,10)
        messagedata = "server#{0}".format(publisher_id)
        message = "{0} {1}".format(topic, messagedata)
        logging.warning("Server publisher_id {0} publish message {1}".format(publisher_id, message))
        socket.send(message)
        time.sleep(1)

def server_router(frontend_port, backend_port):
    '''
        ROUTER process
    '''
    # Prepare context and sockets
    context = zmq.Context()
    #context = zmq.Context.instance()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:{0}".format(frontend_port))

    backend = context.socket(zmq.ROUTER)
    backend.bind("tcp://*:{0}".format(backend_port))

    NBR_CLIENTS = 10

    # Initialize main loop state
    count = NBR_CLIENTS
    workers = []

    while True:
        request = backend.recv_multipart()

        worker, empty, client = request[:3]
        workers.append(worker)
        if client != b"READY" and len(request) > 3:
            # If client reply, send rest back to frontend
            empty, reply = request[3:]
            frontend.send_multipart([client, b"", reply])
            count -= 1
            if not count:
                break

        # Get next client request, route to last-used worker
        client, empty, request = frontend.recv_multipart()
        worker = workers.pop(0)
        backend.send_multipart([worker, b"", client, b"", request])


     # Clean up
    backend.close()
    frontend.close()
    context.term()




def client_dealer(por="5559"):
    '''
        DEALER process
    '''
    pass

def client(port_push, port_sub):
    '''
        Client process
    '''
    context = zmq.Context()
    socket_pull = context.socket(zmq.PULL)
    socket_pull.connect("tcp://localhost:%s" % port_push)
    stream_pull = zmqstream.ZMQStream(socket_pull)
    stream_pull.on_recv(get_command)
    logging.warning("Connected to pull server with port {0}".format(port_push))

    socket_sub = context.socket(zmq.SUB)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    socket_sub.setsockopt(zmq.SUBSCRIBE, "9")
    stream_sub = zmqstream.ZMQStream(socket_sub)
    stream_sub.on_recv(process_message)
    logging.warning("Connected to publisher with port {0}".format(port_sub))

    ioloop.IOLoop.instance().start()
    logging.warning("Worker has stopped processing messages.")

def spawn(message):
    '''
        Spawn process, return new uuid
    '''
    logging.info("Spawn process {0}".format(message))

def link(message):
    '''
        Link processes
    '''
    logging.info("Link processes {0}".format(message))

def spawn_link(message):
    '''
        Spawn link processes
    '''
    logging.info("Spawn new process, {0} return Received process uuid".format(message))

def monitor(message):
    '''
        Monitor processes
    '''
    logging.info("Monitor processes {0}".format(message))

def spawn_monitor(message):
    '''
        Spawn monitor processes
    '''
    logging.info("Spawn new process, {0} return Received process uuid".format(message))

def register(message):
    '''
        Register process uuid
    '''
    logging.info("Received message: %s" % message)

def context_switch(message):
    '''
        Node context switch
    '''
    logging.info("talk between nodes")