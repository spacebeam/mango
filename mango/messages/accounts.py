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



class RequiredBase(models.Model):
    '''
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    active = types.BooleanType(default=True)
    status = types.StringType(required=False)
    account = types.StringType(required=True)
    name = types.StringType(required=False)
    email = types.EmailType(required=True)
    is_admin = types.BooleanType(default=False)
    phone_number = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    location = types.StringType()
    resources = compound.ModelType(Resource)
    
    routes = compound.ListType(compound.ModelType(Route))
    url = types.URLType(required=False)

    # move this to howler and spider?
    max_channels = types.IntType()

class CleanBase(models.Model):
    '''
    '''
    uuid = types.UUIDType()
    active = types.BooleanType()
    status = types.StringType()
    account = types.StringType()
    name = types.StringType()
    email = types.EmailType()
    is_admin = types.BooleanType()
    phone_number = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    location = types.StringType()
    resources = compound.ModelType(Resource)
    
    routes = compound.ListType(compound.ModelType(Route))

    url = types.URLType()

    # move this to howler or spider?
    max_channels = types.IntType()

class BaseAccount(models.Model):
    '''
        Base account
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    active = types.BooleanType(default=True)
    status = types.StringType(required=False)
    account = types.StringType(required=True)
    name = types.StringType(required=False)
    email = types.EmailType(required=True)
    is_admin = types.BooleanType(default=False)
    phone_number = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    location = types.StringType()
    resources = compound.ModelType(Resource)
    
    routes = compound.ListType(compound.ModelType(Route))

    uri = types.StringType(required=False)
    url = types.URLType() #?

    # move this to howler and spider?
    max_channels = types.IntType()


class User(BaseAccount):
    '''
        User account
    '''
    first_name = types.StringType()
    last_name = types.StringType()
    account_type = types.StringType(default='user')
    orgs = compound.ListType(types.StringType())
    password = types.StringType(required=True)
    
    # move company to baseAccount class?
    company = types.StringType()

    # clx stuff, please move this to another place that makes more sense.
    UserId = types.IntType()
    AccountNum = types.StringType()


class ModifyUser(BaseAccount):
    '''
        Modify account
    '''
    account_type = types.StringType(default='user')
    orgs = compound.ListType(types.StringType())
    password = types.StringType()
    
    # move company to baseAccount class?
    company = types.StringType()

    # clx stuff, please move this to another place that makes more sense.
    UserId = types.IntType()
    AccountNum = types.StringType()


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
    description = types.StringType()


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