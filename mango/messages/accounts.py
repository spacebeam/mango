# -*- coding: utf-8 -*-
'''
    Mango accounts models
'''
# This file is part of mango.
#
# Distributed under the terms of the last AGPL License. The full
# license is in the file LICENCE, distributed as part of this
# software.

__author__ = 'Jean Chassoul'


import uuid

from schematics import models
from schematics import types
from schematics.types import compound



class SimpleResource(models.Model):
    '''
        Mango simple resource
    '''
    contains = compound.ListType(types.UUIDType())

    total = types.IntType()


class Resource(models.Model):
    ''' 
        Mango resource
    '''
    apps = compound.ModelType(SimpleResource)
    calls = compound.ModelType(SimpleResource)
    queues = compound.ModelType(SimpleResource)
    records = compound.ModelType(SimpleResource)

    total = types.IntType()


class Route(models.Model):
    '''
        Mango route

        Route model used by the record
    '''
    destination = types.StringType(default='*') 
    dst = types.StringType(default='*') # default '*' means all destinations
    
    channel = types.StringType(required=True)
    dstchannel = types.StringType(required=True)
    destination_channel = types.StringType(required=True)

    cost = types.FloatType(required=True)


class Team(models.Model):
    '''
        Mango team

        iOrganizations team model
    '''
    name = types.StringType(required=True)
    members = compound.ListType(types.StringType())
    permission = types.StringType(choices=['read',
                                           'write',
                                           'super'], required=True)
    resources = compound.ModelType(Resource)


class AccountResource(models.Model):
    '''
        Account resource
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
    account = types.StringType(required=False)
    resource  = types.StringType(required=True)
    

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
  
    
class Org(BaseAccount):
    '''
        Mango (ORG) Organization of Restricted Generality.
    '''
    account_type = types.StringType(default='org')
    # TODO: check members, teams D: 
    members = compound.ListType(types.StringType())
    teams = compound.ListType(compound.ModelType(Team))