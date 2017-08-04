# -*- coding: utf-8 -*-
'''
    Starfruit extensions message models.
'''

# This file is part of starfruit.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__authors__ = ['Jean Chassoul', 'Anthony Solorzano Lopez']


import uuid
import arrow
from schematics import models
from schematics import types
from schematics.types import compound


class Account(models.Model):
    '''
        extension schema
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType(required=True)
    status = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    updated_by = types.StringType()
    updated_at = types.TimestampType()
    change_history = compound.ListType(types.StringType())
    tags = compound.ListType(types.StringType())
    snapshots = compound.ListType(types.StringType())
    addresses = compound.ListType(types.StringType())

class ModifyAccount(models.Model):
    '''
        Modify extension schema

        This model is similar to extension.

        It lacks of require and default values on it's fields.

        The reason of it existence is that we need to validate
        every input data that came from outside the system, with 
        this we prevent users from using PATCH to create fields 
        outside the scope of the resource.
    '''
    uuid = types.UUIDType()
    account = types.StringType()
    status = types.StringType()
    created_at = types.TimestampType()
    created_by = types.StringType()
    created_at = types.TimestampType()
    updated_by = types.StringType()
    updated_at = types.TimestampType()
    change_history = compound.ListType(types.StringType())
    tags = compound.ListType(types.StringType())
    snapshots = compound.ListType(types.StringType())
    addresses = compound.ListType(types.StringType())