# This file is part of mango.

# Distributed under the terms of the last AGPL License.


__author__ = 'Jean Chassoul'


import uuid

from schematics import types
from schematics.types import compound

from mango.schemas import RequiredBase


class BaseAccount(RequiredBase):
    '''
        Base account
    '''
    uuid = types.UUIDType(default=uuid.uuid4)


class User(BaseAccount):
    '''
        User account
    '''
    role = types.StringType(
        choices=['admin', 'user'],
        default='user',
        required=True
    )
    account_type = types.StringType(
        choices=['user', ],
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


class ModifyUser(BaseAccount):
    '''
        Modify account
    '''
    account_type = types.StringType(
        choices=['user', ],
        default='user'
    )
    role = types.StringType(
        choices=['user', ],
        default='user'
    )
    nickname = types.StringType()
    first_name = types.StringType()
    middle_name = types.StringType()
    last_name = types.StringType()
    password = types.StringType()
    orgs = compound.ListType(types.DictType(types.StringType))
    teams = compound.ListType(types.DictType(types.StringType))


class Org(BaseAccount):
    '''
        Org account
    '''
    account_type = types.StringType(
        choices=['org', ],
        default='org',
        required=True
    )
    name = types.StringType()
    description = types.StringType()
    members = compound.ListType(types.StringType())
    owners = compound.ListType(types.StringType())
    teams = compound.ListType(types.DictType(types.StringType))


class ModifyOrg(BaseAccount):
    '''
        ModifyOrg account
    '''
    account_type = types.StringType(
        choices=['org', ],
        default='org'
    )
    name = types.StringType()
    description = types.StringType()
    members = compound.ListType(types.StringType())
    owners = compound.ListType(types.StringType())
    teams = compound.ListType(types.DictType(types.StringType))
