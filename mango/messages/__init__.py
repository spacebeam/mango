# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


from schematics import models
from schematics import types
from schematics.types import compound


class BaseQueue(models.Model):
    '''
        Base queue
    '''
    name = models.CharField(unique=True, max_length=255)
    musiconhold = models.CharField(max_length=384, blank=True, default='default')
    announce = models.CharField(max_length=384, blank=True)
    context = models.CharField(max_length=384, blank=True)
    timeout = models.IntegerField(null=True, blank=True, default=15)
    monitor_join = models.IntegerField(null=True, blank=True, default=1)
    monitor_format = models.CharField(max_length=384, blank=True, default='wav')
    queue_youarenext = models.CharField(max_length=384, blank=True, default='queue-youarenext')
    queue_thereare = models.CharField(max_length=384, blank=True)
    queue_callswaiting = models.CharField(max_length=384, blank=True)
    queue_holdtime = models.CharField(max_length=384, blank=True)
    queue_minutes = models.CharField(max_length=384, blank=True)
    queue_seconds = models.CharField(max_length=384, blank=True)
    queue_lessthan = models.CharField(max_length=384, blank=True, default='queue-less-than')
    queue_thankyou = models.CharField(max_length=384, blank=True, default='queue-thankyou')
    queue_reporthold = models.CharField(max_length=384, blank=True, default='queue-reporthold')
    announce_frequency = models.IntegerField(null=True, blank=True, default=0)
    announce_round_seconds = models.IntegerField(null=True, blank=True, default=10)
    announce_holdtime = models.CharField(max_length=384, blank=True, default='yes')
    retry = models.IntegerField(null=True, blank=True, default=5)
    wrapuptime = models.IntegerField(null=True, blank=True, default=0)
    maxlen = models.IntegerField(null=True, blank=True, default=0)
    servicelevel = models.IntegerField(null=True, blank=True)
    strategy = models.CharField(max_length=384, blank=True, default='rrmemory')
    joinempty = models.CharField(max_length=384, blank=True, default='yes')
    leavewhenempty = models.CharField(max_length=384, blank=True)
    eventmemberstatus = models.IntegerField(null=True, blank=True, default=1)
    eventwhencalled = models.IntegerField(null=True, blank=True, default=1)
    reportholdtime = models.IntegerField(null=True, blank=True, default=1)
    memberdelay = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    timeoutrestart = models.IntegerField(null=True, blank=True)
    periodic_announce = models.CharField(max_length=150, blank=True)
    periodic_announce_frequency = models.IntegerField(null=True, blank=True)
    ringinuse = models.IntegerField(null=True, blank=True, default=0)
    setinterfacevar = models.IntegerField(null=True, blank=True, default=1)


class QueueMember(models.Model):
    '''
        Queue member
    '''
    membername = models.CharField(max_length=120)
    queue_name = models.CharField(max_length=384)
    interface = models.CharField(max_length=384)
    penalty = models.IntegerField(null=True, blank=True)
    paused = models.IntegerField(null=True, blank=True)


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