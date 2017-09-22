# -*- coding: utf-8 -*-
'''
    Mango accounts models and messages.
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
from mango.messages import Resource


class Email(models.Model):
    '''
        Email
    '''
    title = types.StringType()
    address = types.EmailType()
    validated = types.BooleanType(default=False)
    primary = types.BooleanType(default=False)


class Phone(models.Model):
    '''
        Phone
    '''
    title = types.StringType()
    number = types.StringType()
    extension = types.StringType()
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
    permission = types.StringType()
    phone_number = types.StringType()
    extension = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    company = types.StringType()
    location = types.StringType()
    phones = compound.ListType(compound.ModelType(Phone))
    emails = compound.ListType(compound.ModelType(Email))
    uri = types.URLType(required=False)
    max_channels = types.IntType()
    checksum = types.StringType()
    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    labels =  compound.ListType(types.StringType())
    labels_total = types.IntType()
    resources = compound.ModelType(Resource)
    resources_total = types.IntType()
    history = compound.ListType(types.StringType())
    history_total = types.IntType()
    hashs = compound.ListType(types.StringType())
    hashs_total = types.IntType()

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
    permission = types.StringType()
    phone_number = types.StringType()
    extension = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    company = types.StringType()
    location = types.StringType()
    phones = compound.ListType(compound.ModelType(Phone))
    emails = compound.ListType(compound.ModelType(Email))
    uri = types.URLType()
    max_channels = types.IntType()
    checksum = types.StringType()
    checked = types.BooleanType()
    checked_by = types.StringType()
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    labels =  compound.ListType(types.StringType())
    labels_total = types.IntType()
    resources = compound.ModelType(Resource)
    resources_total = types.IntType()
    history = compound.ListType(types.StringType())
    history_total = types.IntType()
    hashs = compound.ListType(types.StringType())
    hashs_total = types.IntType()

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
    layout = types.StringType()
    powerdailer = types.StringType()
    lead_access = types.StringType()
    phone_server_register = types.StringType()

class ModifyUser(CleanBaseAccount):
    '''
        Modify account
    '''
    first_name = types.StringType()
    last_name = types.StringType()
    account_type = types.StringType(default='user')
    orgs = compound.ListType(types.StringType())
    password = types.StringType()
    layout = types.StringType()
    powerdailer = types.StringType()
    lead_access = types.StringType()
    phone_server_register = types.StringType()


class Team(models.Model):
    '''
        Org team
    '''
    uuid = types.UUIDType(default=uuid.uuid4)
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
    members = compound.ListType(types.StringType())
    teams = compound.ListType(compound.ModelType(Team))