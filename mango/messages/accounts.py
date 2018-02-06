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
    phone_number = types.StringType()
    extension = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    company = types.StringType()
    location = types.StringType()
    url = types.URLType(required=False)
    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    phones = compound.ListType(compound.ModelType(Phone))
    emails = compound.ListType(compound.ModelType(Email))
    labels = compound.ListType(types.StringType())
    history = compound.ListType(types.StringType())
    hashs = compound.ListType(types.StringType())
    watchers = compound.ListType(types.StringType())


class CleanBase(models.Model):
    '''
        Clean base class
    '''
    active = types.BooleanType()
    status = types.StringType()
    account = types.StringType()
    name = types.StringType()
    email = types.EmailType()
    phone_number = types.StringType()
    extension = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    company = types.StringType()
    location = types.StringType()
    url = types.URLType()
    checked = types.BooleanType()
    checked_by = types.StringType()
    checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)
    created_by = types.StringType()
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    phones = compound.ListType(compound.ModelType(Phone))
    emails = compound.ListType(compound.ModelType(Email))
    labels = compound.ListType(types.StringType())
    history = compound.ListType(types.StringType())
    hashs = compound.ListType(types.StringType())
    watchers = compound.ListType(types.StringType())


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
    account_type = types.StringType(default='user')
    first_name = types.StringType()
    last_name = types.StringType()
    password = types.StringType(required=True)
    orgs = compound.ListType(types.StringType())


class ModifyUser(CleanBaseAccount):
    '''
        Modify account
    '''
    account_type = types.StringType(default='user')
    first_name = types.StringType()
    last_name = types.StringType()
    password = types.StringType()
    orgs = compound.ListType(types.StringType())


class Org(BaseAccount):
    '''
        Org account
    '''
    account_type = types.StringType(default='org')
    members = compound.ListType(types.StringType())
    teams = compound.ListType(compound.ModelType(Team))
