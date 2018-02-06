# -*- coding: utf-8 -*-
'''
    Mango teams models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import arrow
import uuid
from schematics import models
from schematics import types
from schematics.types import compound


class Team(models.Model):
    '''
       (ORG) Team
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType()
    status = types.StringType()
    name = types.StringType(required=True)
    permission = types.StringType(choices=['read',
                                           'write',
                                           'admin'], required=True)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    url = types.URLType()
    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    members = compound.ListType(types.StringType())
    hashs = compound.ListType(types.StringType())
    labels = compound.ListType(types.StringType())
    history = compound.ListType(types.StringType())
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)
    active = types.BooleanType(default=True)


class ModifyTeam(models.Model):
    '''
        Modify (ORG) Team
    '''
    uuid = types.UUIDType()
    account = types.StringType()
    status = types.StringType()
    name = types.StringType()
    permission = types.StringType()
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    url = types.URLType()
    checked = types.BooleanType()
    checked_by = types.StringType()
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    members = compound.ListType(types.StringType())
    hashs = compound.ListType(types.StringType())
    labels = compound.ListType(types.StringType())
    history = compound.ListType(types.StringType())
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)
    active = types.BooleanType()
