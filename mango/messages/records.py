# -*- coding: utf-8 -*-
'''
    Mango records models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import arrow
import uuid

from schematics import models
from schematics import types
from schematics.types import compound


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


class Comment(models.Model):
    '''
        Comment class
    '''
    comment = types.StringType()


class Record(models.Model):
    '''
        Record Object Data Structure
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    uniqueid = types.StringType()

    clid = types.StringType()
    callerid = types.StringType()

    account = types.StringType()
    accountcode = types.StringType()
    userfield = types.StringType()

    queue = compound.ModelType(FromQueue)
    
    assigned = types.BooleanType(default=False)
    checked = types.BooleanType(default=False)

    public = types.BooleanType(default=False)

    source = types.StringType()
    destination = types.StringType()
    
    channel = types.StringType()
    source_channel = types.StringType()
    
    context = types.StringType()
    dcontext = types.StringType()
    destination_context = types.StringType()

    destination_number = types.StringType()
    
    dstchannel = types.StringType()
    destination_channel = types.StringType()
    
    start = types.DateTimeType()
    answer = types.DateTimeType()
    end = types.DateTimeType()

    duration = types.IntType()
    billsec = types.IntType()
    billing = types.IntType()

    disposition = types.StringType()
    status = types.StringType()

    amaflags = types.StringType()

    lastapp = types.StringType()
    lastdata = types.StringType()

    recorded = types.BooleanType(default=False)
    record_uri = types.StringType()

    checked = types.BooleanType(default=False)
    checked_by = types.StringType()

    #details = compound.ModelType(Log)
    #comments = compound.ModelType(Comment)
    
    created = types.DateTimeType(default=arrow.utcnow().naive)
    #created_at = types.DateTimeType()
    last_modified = types.DateTimeType()
    updated_by = types.DateTimeType()
    updated_at = types.DateTimeType()

    uri = types.StringType()