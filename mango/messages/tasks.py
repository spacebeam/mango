# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Space Beam'


import arrow
import uuid
from schematics import models
from schematics import types
from schematics.types import compound


class Task(models.Model):
    '''
        Task Data Structure
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType(required=True)
    name = types.StringType()
    description = types.StringType()
    data = types.StringType()
    assign = compound.ListType(types.StringType())
    public = types.BooleanType(default=False)
    source = types.StringType()
    destination = types.StringType()
    labels = types.DictType(types.StringType)
    start_time = types.TimestampType()
    ack_time = types.TimestampType()
    stop_time = types.TimestampType()
    deadline = types.TimestampType()
    duration = types.StringType()
    status = types.StringType(choices=['new',
                                       'now',
                                       'later',
                                       'done'],
                              default='new',
                              required=True)
    history = compound.ListType(types.StringType())
    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    last_update_by = types.StringType()
    last_update_at = types.TimestampType()


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
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType()
    name = types.StringType()
    description = types.StringType()
    data = types.StringType()
    assign = compound.ListType(types.StringType())
    public = types.BooleanType(default=False)
    source = types.StringType()
    destination = types.StringType()
    labels = types.DictType(types.StringType)
    start_time = types.TimestampType()
    ack_time = types.TimestampType()
    stop_time = types.TimestampType()
    deadline = types.TimestampType()
    duration = types.StringType()
    status = types.StringType(choices=['new',
                                       'now',
                                       'later',
                                       'done'],
                              default='new',
                              required=True)
    history = compound.ListType(types.StringType())
    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    last_update_by = types.StringType()
    last_update_at = types.TimestampType()
