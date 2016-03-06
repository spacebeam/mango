# -*- coding: utf-8 -*-
'''
    Mango accounts models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import arrow
import uuid

from schematics import models
from schematics import types
from schematics.types import compound

from mango.messages import Resource



class Membership(models.Model):
    '''
        Org membership
    '''
    username = types.StringType(required=True)
    status = types.StringType(default='pending')
    role = types.StringType(required=True)
    org = types.StringType(required=True)
    created = types.UTCDateTimeType(default=arrow.utcnow().naive)


class ModifyMembership(models.Model):
    '''
        Modify membership

        This model is similar to membership.

        It lacks of require and default values on it's fields.

        The reason of it existence is that we need to validate
        every input data that came from outside the system, with 
        this we prevent users from using PATCH to create fields 
        outside the scope of the resource.
    '''
    username = types.StringType()
    status = types.StringType()
    role = types.StringType()
    org = types.StringType()
    created = types.UTCDateTimeType()


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


class Email(models.Model):
    '''
        Email
    '''
    address = types.EmailType()
    validated = types.BooleanType(default=False)
    primary = types.BooleanType(default=False)


class RequiredBase(models.Model):
    '''
        Required base class
    '''
    active = types.BooleanType(default=True)
    status = types.StringType(required=False)
    account = types.StringType(required=True)
    name = types.StringType(required=False)
    email = types.EmailType(required=True)
    is_admin = types.BooleanType(default=False)
    domain = types.StringType()
    phone_number = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    company = types.StringType()
    location = types.StringType()
    resources = compound.ModelType(Resource)
    routes = compound.ListType(compound.ModelType(Route))
    emails = compound.ListType(compound.ModelType(Email))
    url = types.URLType(required=False)
    max_channels = types.IntType()
    created_at = types.DateTimeType(default=arrow.utcnow().naive)


class CleanBase(models.Model):
    '''
        Clean base class
    '''
    active = types.BooleanType()
    status = types.StringType()
    account = types.StringType()
    name = types.StringType()
    email = types.EmailType()
    is_admin = types.BooleanType()
    phone_number = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    company = types.StringType()
    location = types.StringType()
    resources = compound.ModelType(Resource)
    routes = compound.ListType(compound.ModelType(Route))
    emails = compound.ListType(compound.ModelType(Email))
    url = types.URLType()
    max_channels = types.IntType()
    created_at = types.DateTimeType()


class BaseAccount(RequiredBase):
    '''
        Base account
    '''
    uuid = types.UUIDType(default=uuid.uuid4)


class CleanBaseAccount(CleanBase):
    '''
        Clean base account
    '''
    uuid = types.UUIDType()


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


class ModifyUser(CleanBaseAccount):
    '''
        Modify account
    '''
    first_name = types.StringType()
    last_name = types.StringType()
    account_type = types.StringType(default='user')
    orgs = compound.ListType(types.StringType())
    password = types.StringType()

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