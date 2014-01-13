# -*- coding: utf-8 -*-
'''
    Mango records data models
'''
# This file is part of mango.
#
# Distributed under the terms of the last AGPL License. The full
# license is in the file LICENCE, distributed as part of this
# software.

__author__ = 'Jean Chassoul'


import uuid

from schematics import models
from schematics import types
from schematics.types import compound

from schematics.contrib import mongo


class FromQueue(models.Model):
    '''
        Mango from queue

        Call from a ACD Queue configuration class
    '''
    queue_name = types.StringType()
    on_queue_duration = types.IntType()
    with_agent_duration = types.IntType()
    enter_time = types.DateTimeType()
    answer_time = types.DateTimeType()
    hangup_time = types.DateTimeType()


class Record(models.Model):
    '''
        Mango record
        
        Record Object Data Structure
    '''
    _id = mongo.ObjectIdType(required=False)

    uuid = types.UUIDType(default=uuid.uuid4)

    accountcode = types.StringType()
    
    # assigned record flag
    assigned = types.BooleanType(default=False)

    # TODO: checked flag (future)
    checked = types.BooleanType(default=False)

    # the public flag shows if the record record is public
    # and can be seen be every user account
    public = types.BooleanType(default=False)


    source = types.StringType()
    destination = types.StringType()

    source_channel = types.StringType()
    destination_channel = types.StringType()


    src = types.StringType()
    dst = types.StringType()
    dcontext = types.StringType()
    clid = types.StringType()
    channel = types.StringType()
    dstchannel = types.StringType()
    lastapp = types.StringType()
    lastdata = types.StringType()
    start = types.DateTimeType(required=True)
    answer = types.DateTimeType()
    end = types.DateTimeType()
    duration = types.IntType()
    billsec = types.IntType()
    disposition = types.StringType()
    amaflags = types.StringType()
    uniqueid = types.StringType()
    userfield = types.StringType()
    
    queue = compound.ModelType(FromQueue)
    
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