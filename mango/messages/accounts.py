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



class AccountResource(models.Model):
    '''
        Account resource
    '''
    account = types.StringType(required=False)
    uuid = types.UUIDType(default=uuid.uuid4)
    resource  = types.StringType(required=True)


class Route(models.Model):
    '''
        Mango route
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
        Mango base account
    '''
    uuid = types.UUIDType(default=uuid.uuid4)

    active = types.BooleanType(default=True)
    account = types.StringType(required=True)
    name = types.StringType(required=False)
    email = types.EmailType(required=True)
    url = types.URLType()
    
    # TODO: Geolocation stuff

    # location = StringType(required=True)
    # timezone = StringType(required=True)
    
    resources = compound.ModelType(Resource)
    routes = compound.ListType(compound.ModelType(Route))


class User(BaseAccount):
    '''
        Mango user
    '''
    account_type = types.StringType(default='user')
    orgs = compound.ListType(types.StringType())
    password = types.StringType(required=True)
    
    # move company to baseAccount class?
    company = types.StringType()


class Team(models.Model):
    '''
        ORGs team
    '''
    name = types.StringType(required=True)
    members = compound.ListType(types.StringType())
    permission = types.StringType(choices=['read',
                                           'write',
                                           'super'], required=True)
    resources = compound.ModelType(Resource)
  
    
class Org(BaseAccount):
    '''
        Mango (ORG) Organization of Restricted Generality.
    '''
    account_type = types.StringType(default='org')
    
    # tests for members and teams.
    members = compound.ListType(types.StringType())
    teams = compound.ListType(compound.ModelType(Team))