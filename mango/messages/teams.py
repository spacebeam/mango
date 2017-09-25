# -*- coding: utf-8 -*-
'''
    Mango teams models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Nonsense'


import arrow
import uuid
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
    status = types.StringType()
    name = types.StringType(required=True)
    permission = types.StringType(choices=['read',
                                           'write',
                                           'admin'], required=True)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)
    uri = types.URLType()
    checksum = types.StringType()
    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    members = compound.ListType(types.StringType())
    members_total = types.IntType()
    hashs = compound.ListType(types.StringType())
    hashs_total = types.IntType()    
    resources = compound.ModelType(Resource)
    resources_total = types.IntType()
    labels = compound.ListType(types.StringType())
    labels_total = types.IntType()
    history = compound.ListType(types.StringType())
    history_total = types.IntType()


class ModifyTeam(models.Model):
    '''
        Team
    '''
    uuid = types.UUIDType()
    account = types.StringType()
    status = types.StringType()
    name = types.StringType()
    permission = types.StringType()
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)
    uri = types.URLType()
    checksum = types.StringType()
    checked = types.BooleanType()
    checked_by = types.StringType()
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    members = compound.ListType(types.StringType())
    members_total = types.IntType()
    hashs = compound.ListType(types.StringType())
    hashs_total = types.IntType()    
    resources = compound.ModelType(Resource)
    resources_total = types.IntType()
    labels = compound.ListType(types.StringType())
    labels_total = types.IntType()
    history = compound.ListType(types.StringType())
    history_total = types.IntType()