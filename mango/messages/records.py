# -*- coding: utf-8 -*-
'''
    Mango records models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import uuid

from schematics import models
from schematics import types
from schematics.types import compound

from schematics.contrib import mongo


class FromQueue(models.Model):
    '''
        from a ACD Queue
    '''
    queue_name = types.StringType()
    on_queue_duration = types.IntType()
    with_agent_duration = types.IntType()
    enter_time = types.DateTimeType()
    answer_time = types.DateTimeType()
    hangup_time = types.DateTimeType()


class Record(models.Model):
    '''
        Record Object Data Structure
    '''
    _id = mongo.ObjectIdType(required=False)
    uuid = types.UUIDType(default=uuid.uuid4)

    clid = types.StringType()

    uniqueid = types.StringType()
    queue = compound.ModelType(FromQueue)

    accountcode = types.StringType()
    userfield = types.StringType()
    
    assigned = types.BooleanType(default=False)
    checked = types.BooleanType(default=False)

    public = types.BooleanType(default=False)

    source = types.StringType()
    destination = types.StringType()

    source_channel = types.StringType()
    destination_channel = types.StringType()

    src = types.StringType()
    dst = types.StringType()
    dcontext = types.StringType()
    
    channel = types.StringType()
    dstchannel = types.StringType()
    
    start = types.DateTimeType(required=True)
    answer = types.DateTimeType()
    end = types.DateTimeType()

    duration = types.IntType()
    billsec = types.IntType()
    disposition = types.StringType()
    amaflags = types.StringType()

    lastapp = types.StringType()
    lastdata = types.StringType()
    
    # TODO: CEL events
    # events
    # recorded = BooleanType()
    # record_url
    # checked
    # checked_by
    # details
    # comments
    # created
    # last_modify
    # updated_by