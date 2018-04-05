# -*- coding: utf-8 -*-
'''
    Mango teams message models.
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
    # Yo, this MUST be an organization account!
    account = types.StringType(required=True)
    status = types.StringType(required=True)
    name = types.StringType(required=True)
    description = types.StringType()
    permission = types.StringType(choices=['read',
                                           'write',
                                           'owner'], required=True)
    members = compound.ListType(types.StringType(), required=True)
    resources = compound.ListType(types.StringType()) # [resource:uuid, noun:*]
    labels = compound.ListType(types.StringType())
    history = compound.ListType(types.StringType())
    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    checked_at = types.TimestampType()
    created_by = types.StringType(required=True)
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    last_update_by = types.StringType()
    last_update_at = types.TimestampType()


class ModifyTeam(models.Model):
    '''
        Modify (ORG) Team
    '''
    uuid = types.UUIDType()
    # Yo, this MUST be an organization account!
    account = types.StringType()
    status = types.StringType()
    name = types.StringType()
    description = types.StringType()
    permission = types.StringType()
    members = compound.ListType(types.StringType())
    resources = compound.ListType(types.StringType())
    labels = compound.ListType(types.StringType())
    history = compound.ListType(types.StringType())
    checked = types.BooleanType()
    checked_by = types.StringType()
    checked_at = types.TimestampType()
    created_by = types.StringType()
    created_at = types.TimestampType()
    last_update_by = types.StringType()
    last_update_at = types.TimestampType()
