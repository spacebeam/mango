# -*- coding: utf-8 -*-
'''
    Mango accounts models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Nonsense'



import uuid
import arrow
from schematics import models
from schematics import types
from schematics.types import compound
from mango.messages import Resource


class Team(models.Model):
    '''
       Team
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType(required=True)
    name = types.StringType(required=True)
    permission = types.StringType(choices=['read',
                                           'write',
                                           'admin'], required=True)
    members = compound.ListType(types.StringType())
    resources = compound.ModelType(Resource)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    last_update_by = types.StringType()
    last_update_at = types.TimestampType()
    history = compound.ListType(types.StringType())
    labels = compound.ListType(types.StringType())
    snapshots = compound.ListType(types.StringType())
    addresses = compound.ListType(types.StringType())
    status = types.StringType()

class ModifyTeam(models.Model):
    '''
        Team
    '''
    uuid = types.UUIDType()
    account = types.StringType()
    name = types.StringType()
    permission = types.StringType()
    members = compound.ListType(types.StringType())
    resources = compound.ModelType(Resource)
    created_by = types.StringType()
    created_at = types.TimestampType()
    last_update_by = types.StringType()
    last_update_at = types.TimestampType()
    history = compound.ListType(types.StringType())
    labels = compound.ListType(types.StringType())
    snapshots = compound.ListType(types.StringType())
    addresses = compound.ListType(types.StringType())
    status = types.StringType()