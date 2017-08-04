# -*- coding: utf-8 -*-
'''
    Team message models.
'''

# This file is part of cas.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import uuid
import arrow
from schematics import models
from schematics import types
from schematics.types import compound


class Team(models.Model):
    '''
        Team messages
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType(required=True)
    source = types.StringType()
    comment = types.StringType()
    resource = types.StringType()
    sentiment = types.StringType()
    ranking = types.StringType()
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    updated_by = types.StringType()
    updated_at = types.TimestampType()
    change_history = compound.ListType(types.StringType())
    tags = compound.ListType(types.StringType())
    snapshots = compound.ListType(types.StringType())
    addresses = compound.ListType(types.StringType())
    status = types.StringType()
    

class ModifyTeam(models.Model):
    '''
        Modify Team

        This model is similar to event.

        It lacks of require and default values on it's fields.

        The reason of it existence is that we need to validate
        every input data that came from outside the system, with 
        this we prevent users from using PATCH to create fields 
        outside the scope of the resource.
    '''
    uuid = types.UUIDType()
    account =types.StringType()
    source = types.StringType()
    comment = types.StringType()
    resource = types.StringType()
    sentiment = types.StringType()
    ranking = types.StringType()
    created_by = types.StringType()
    created_at = types.TimestampType()
    updated_by = types.StringType()
    updated_at = types.TimestampType()
    change_history = compound.ListType(types.StringType())
    tags = compound.ListType(types.StringType())
    snapshots = compound.ListType(types.StringType())
    addresses = compound.ListType(types.StringType())
    status = types.StringType()