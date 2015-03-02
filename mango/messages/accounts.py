# -*- coding: utf-8 -*-
'''
    Mango accounts models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import uuid

from schematics import models
from schematics import types
from schematics.types import compound

from mango.messages import Resource


class Password(models.Model):
    '''
        Password
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    assigned = types.BooleanType(default=False)
    password = types.StringType()
    raw = types.StringType()
    md5 = types.StringType()
    sha1 = types.StringType()
    sha256 = types.StringType()
    sha384 = types.StringType()
    sha512 = types.StringType()
    created_at = types.DateTimeType()
    last_modified = types.DateTimeType()


#class Mon(models.Model):
#    '''
#        Monkey business
#    '''
#    key = types.StringType(required=True)


class Route(models.Model):
    '''
        Route
    '''
    # default '*' means all destinations
    
    dst = types.StringType(default='*')
    destination = types.StringType(default='*') 

    channel = types.StringType(required=True)

    dstchannel = types.StringType(required=True)
    destination_channel = types.StringType(required=True)

    cost = types.FloatType(required=True)


class BaseAccount(models.Model):
    '''
        Base account
    '''
    uuid = types.UUIDType(default=uuid.uuid4)

    passwords = compound.ListType(compound.ModelType(Password))

    # api samples, remove after finish work on passwords or otherwise secret keys.
    api_key = types.StringType(required=False)
    # api_keys = compound.ListType(compound.ModelType(Mon))

    active = types.BooleanType(default=True)
    account = types.StringType(required=True)
    name = types.StringType(required=False)
    email = types.EmailType(required=True)
    timezone = types.StringType()

    resources = compound.ModelType(Resource)
    
    routes = compound.ListType(compound.ModelType(Route))

    uri = types.StringType(required=False)
    url = types.URLType()

    # move this to howler and spider?
    max_channels = types.IntType()


class User(BaseAccount):
    '''
        User account
    '''
    account_type = types.StringType(default='user')
    orgs = compound.ListType(types.StringType())
    password = types.StringType(required=True)
    
    # move company to baseAccount class?
    company = types.StringType()


class ModifyUser(BaseAccount):
    '''
        Modify account
    '''
    account_type = types.StringType(default='user')
    orgs = compound.ListType(types.StringType())
    password = types.StringType()
    
    # move company to baseAccount class?
    company = types.StringType()


class Team(models.Model):
    '''
        Org team
    '''
    name = types.StringType(required=True)
    permission = types.StringType(choices=['read',
                                           'write',
                                           'admin'], required=True)
    members = compound.ListType(types.StringType())
    resources = compound.ModelType(Resource)


class Org(BaseAccount):
    '''
        Org account
    '''
    account_type = types.StringType(default='org')
    
    # tests for members and teams.
    members = compound.ListType(types.StringType())
    teams = compound.ListType(compound.ModelType(Team))