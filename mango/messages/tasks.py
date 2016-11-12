# -*- coding: utf-8 -*-
'''
    Mango tasks models and messages.
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


class SimpleEntry(models.Model):
    '''
        Simple comment Entry
    '''
    count = types.IntType()
    account = types.StringType()
    comment = types.StringType()
    created_at = types.DateTimeType(default=arrow.utcnow().naive)


class Comment(models.Model):
    ''' 
        Comment
    '''
    comments = compound.ListType(compound.ModelType(SimpleEntry))

    total = types.IntType()


class Task(models.Model):
    '''
        Task Object Data Structure
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType()
    
    assigned = types.BooleanType(default=False)

    public = types.BooleanType(default=False)

    title = types.StringType()

    first_name = types.StringType()
    last_name = types.StringType()
    description = types.StringType()

    data = types.StringType() # a freaking JSON.

    source = types.StringType()
    destination = types.StringType()

    labels = compound.ListType(types.StringType())

    sip = types.StringType()

    email = types.StringType()    

    url = types.StringType()
    
    context = types.StringType()

    destination_context = types.StringType()
    destination_number = types.StringType()
    destination_channel = types.StringType()

    channel = types.StringType()
    from_channel = types.StringType()

    gateway = types.StringType()
    from_gateway = types.StringType()

    start = types.DateTimeType()
    ack = types.DateTimeType()
    end = types.DateTimeType()

    duration = types.IntType()

    comments = compound.ModelType(Comment)

    status = types.StringType(choices=['now',
                                       'later',
                                       'done'],
                              default='now',
                              required=True)

    checked = types.BooleanType(default=False)

    checked_by = types.StringType()
    updated_by = types.StringType()
    updated_at = types.DateTimeType()
    created_at = types.DateTimeType(default=arrow.utcnow().naive)

    last_modified = types.DateTimeType()
    

class ModifyTask(models.Model):
    '''
        Modify task

        This model is similar to Task.

        It lacks of require and default values on it's fields.

        The reason of it existence is that we need to validate
        every input data that came from outside the system, with 
        this we prevent users from using PATCH to create fields 
        outside the scope of the resource.
    '''
    uuid = types.UUIDType()
    title = types.StringType()
    first_name = types.StringType()
    last_name = types.StringType()
    description = types.StringType()
    label = types.StringType()
    category = types.StringType()
    email = types.StringType()
    account = types.StringType()
    accountcode = types.StringType()
    userfield = types.StringType()
    assigned = types.BooleanType()
    checked = types.BooleanType()
    public = types.BooleanType()
    source = types.StringType()
    destination = types.StringType()
    channel = types.StringType()
    source_channel = types.StringType()
    context = types.StringType()
    destination_context = types.StringType()
    destination_number = types.StringType()
    destination_channel = types.StringType()
    start = types.DateTimeType()
    answer = types.DateTimeType()
    end = types.DateTimeType()
    duration = types.IntType()
    billsec = types.IntType()
    billing = types.IntType()
    rate = types.IntType()
    disposition = types.StringType()
    status = types.StringType()
    priority = types.StringType()
    severity = types.StringType()
    checked = types.BooleanType()
    checked_by = types.StringType()
    created_at = types.DateTimeType()
    comments = compound.ModelType(Comment)
    last_modified = types.DateTimeType()
    updated_by = types.StringType()
    updated_at = types.DateTimeType()
    uri = types.StringType()