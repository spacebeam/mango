# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
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

from messages import RequiredBase



class BaseAccount(RequiredBase):
    '''
        Base account
    '''
    uuid = types.UUIDType(default=uuid.uuid4)


class User(BaseAccount):
    '''
        User account
    '''
    account_type = types.StringType(
        choices=['user',],
        default='user',
        required=True
    )
    nickname = types.StringType()
    first_name = types.StringType()
    middle_name = types.StringType()
    last_name = types.StringType()
    password = types.StringType(required=True)
    orgs = compound.ListType(types.DictType(types.StringType))
    teams = compound.ListType(types.DictType(types.StringType))


class Org(BaseAccount):
    '''
        Org account
    '''
    account_type = types.StringType(
        choices=['org',],
        default='org',
        required=True
    )
    name = types.StringType()
    description = types.StringType()
    members = compound.ListType(types.StringType())
    owners = compound.ListType(types.StringType())
    teams = compound.ListType(types.DictType(types.StringType))