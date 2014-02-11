# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'



'''
    Text models are incredibly powerful.
    ------------------------------------

    Maxwell's equations describe classical electrodynamic in four textual equations.

    In some domains pictures are great - show me a photo of a rose, a plan of house, 
    or a set of equations describing the motions of the planets. 

    No one descriptive method is best.

    /Joe
'''

'''
    Messaging pattern
    -----------------

    In software architecture, a messaging pattern is a network-oriented 
    architectural pattern which describes how two different parts of a 
    message passing system connect and communicate with each other.

    In telecommunications, a message exchange pattern (MEP) describes 
    the pattern of messages required by a communications protocol to 
    establish or use a communication channel. 

    There are two major message exchange patterns 

    — a request-response pattern, and a one-way pattern. 

    For example, the HTTP is a request-response 
    pattern protocol, and the UDP has a one-way pattern.
'''

'''
    ØMQ
    ---
    
    ØMQ (also known as ZeroMQ, 0MQ, or zmq) looks like an embeddable networking library
    but acts like a concurrency framework. 

    It gives you sockets that carry atomic messages across various transports 
    like in-process, inter-process, TCP, and multicast. 

    You can connect sockets N-to-N with patterns like fan-out, pub-sub, 
    task distribution, and request-reply.

    Its asynchronous I/O model gives you scalable multicore applications, 
    built as asynchronous message-processing tasks.

'''

'''
    pipes
    -----
    expand on unix pipelines, there is a cool old video on your youtube history about unix and stuff.
'''

'''
    UUID
    ----
    A universally unique identifier (UUID) is an identifier standard 
    for software construction.
'''


from schematics import models
from schematics import types
from schematics.types import compound


class SimpleResource(models.Model):
    '''
        Mango simple resource
    '''
    contains = compound.ListType(types.UUIDType())

    total = types.IntType()


class Resource(models.Model):
    ''' 
        Mango resource
    '''
    # apps = compound.ModelType(SimpleResource)
    # calls = compound.ModelType(SimpleResource)
    # queues = compound.ModelType(SimpleResource)
    records = compound.ModelType(SimpleResource)

    total = types.IntType()