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


class Mon(models.Model):
    '''
        Monkey business
    '''
    key = types.StringType(required=True)


class AccountResource(models.Model):
    '''
        Account resource
    '''
    account = types.StringType(required=False)
    uuid = types.UUIDType(default=uuid.uuid4)
    resource  = types.StringType(required=True)


class Route(models.Model):
    '''
        Route
    '''
    # default '*' means all destinations
    destination = types.StringType(default='*') 
    dst = types.StringType(default='*')
    
    channel = types.StringType(required=True)
    dstchannel = types.StringType(required=True)
    destination_channel = types.StringType(required=True)

    cost = types.FloatType(required=True)


class BaseAccount(models.Model):
    '''
        Base account
    '''
    uuid = types.UUIDType(default=uuid.uuid4)

    api_key = types.StringType(required=False)
    api_keys = compound.ListType(compound.ModelType(Mon))

    active = types.BooleanType(default=True)
    account = types.StringType(required=True)
    name = types.StringType(required=False)
    timezone = types.StringType()
    email = types.EmailType(required=True)
    url = types.URLType()

    resources = compound.ModelType(Resource)
    
    routes = compound.ListType(compound.ModelType(Route))

    uri = types.StringType(required=False)


class User(BaseAccount):
    '''
        User account
    '''
    account_type = types.StringType(default='user')
    orgs = compound.ListType(types.StringType())
    password = types.StringType(required=True)
    
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