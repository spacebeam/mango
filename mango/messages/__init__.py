# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'

import uuid

from schematics import models
from schematics import types
from schematics.types import compound


class CampaignQueue(models.Model):
    '''
        Campaign queue
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    name = types.StringType(required=True)

    musiconhold = types.StringType(default='default')
    announce = types.StringType()
    context = types.StringType()
    timeout = types.IntType(default=15)

    monitor_join = types.IntType(default=1)
    monitor_format = types.StringType(default='wav')

    queue_youarenext = types.StringType(default='queue-youarenext')
    queue_thereare = types.StringType()
    queue_callswaiting = types.StringType()
    queue_holdtime = types.StringType()
    queue_minutes = types.StringType()
    queue_seconds = types.StringType()
    queue_lessthan = types.StringType(default='queue-less-than')
    queue_thankyou = types.StringType(default='queue-thankyou')
    queue_reporthold = types.StringType(default='queue-reporthold')

    announce_frequency = types.IntType()
    announce_round_seconds = types.IntType(default=10)
    announce_holdtime = types.StringType(default='yes')

    retry = types.IntType(default=5)
    wrapuptime = types.IntType()
    maxlen = types.IntType()
    servicelevel = types.IntType()
    strategy = types.StringType(choices=['ringall',
                                         'leastrecent',
                                         'fewestcalls',
                                         'random',
                                         'rrmemory',
                                         'linear',
                                         'wrandom'],
                                required=True)

    joinempty = types.StringType(default='yes')
    leavewhenempty = types.StringType()

    eventmemberstatus = types.IntType(default=1)
    eventwhencalled = types.IntType(default=1)
    reportholdtime = types.IntType(default=1)
    memberdelay = types.IntType()
    weight = types.IntType()
    timeoutrestart = types.IntType()

    periodic_announce = types.StringType()
    periodic_announce_frequency = types.IntType()

    ringinuse = types.IntType(default=0)
    setinterfacevar = types.IntType(default=1)


class QueueMember(models.Model):
    '''
        Queue member
    '''
    membername = types.StringType()
    queue_name = types.StringType()
    interface = types.StringType()
    penalty = types.IntType()
    paused = types.IntType()


class SimpleResource(models.Model):
    '''
        Simple resource
    '''
    contains = compound.ListType(types.UUIDType())

    total = types.IntType()


class Resource(models.Model):
    ''' 
        Resource
    '''
    queues = compound.ModelType(SimpleResource)
    records = compound.ModelType(SimpleResource)

    total = types.IntType()