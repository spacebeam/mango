# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Space Beam LLC'


import arrow
import uuid
from schematics import models
from schematics import types
from schematics.types import compound


class Email(models.Model):
    '''
        Email
    '''
    name = types.StringType()
    address = types.EmailType()
    validated = types.BooleanType(default=False)
    primary = types.BooleanType(default=False)


class Phone(models.Model):
    '''
        Phone
    '''
    name = types.StringType()
    number = types.StringType()
    extension = types.StringType()
    validated = types.BooleanType(default=False)
    primary = types.BooleanType(default=False)


class RequiredBase(models.Model):
    '''
        Required base class
    '''
    status = types.StringType(required=False)
    account = types.StringType(required=True)
    role = types.StringType(required=False)
    email = types.EmailType(required=True)
    phone_number = types.StringType()
    extension = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    company = types.StringType()
    location = types.StringType()
    phones = compound.ListType(compound.ModelType(Phone))
    emails = compound.ListType(compound.ModelType(Email))
    labels = types.DictType(types.StringType)
    history = compound.ListType(types.StringType())
    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    checked_at = types.TimestampType()
    created_by = types.StringType(required=True)
    created_at = types.TimestampType(default=arrow.utcnow().timestamp)
    last_update_by = types.StringType()
    last_update_at = types.TimestampType()


class CleanBase(models.Model):
    '''
        Clean base class
    '''
    status = types.StringType()
    account = types.StringType()
    role = types.StringType()
    email = types.EmailType()
    phone_number = types.StringType()
    extension = types.StringType()
    country_code = types.StringType()
    timezone = types.StringType()
    company = types.StringType()
    location = types.StringType()
    phones = compound.ListType(compound.ModelType(Phone))
    emails = compound.ListType(compound.ModelType(Email))
    labels = types.DictType(types.StringType)
    history = compound.ListType(types.StringType())
    checked = types.BooleanType()
    checked_by = types.StringType()
    checked_at = types.TimestampType()
    created_by = types.StringType()
    created_at = types.TimestampType()
    last_update_by = types.StringType()
    last_update_at = types.TimestampType(default=arrow.utcnow().timestamp)


class BaseResult(models.Model):
    '''
        Base result
    '''
    count = types.IntType()
    page = types.IntType()
    results = compound.ListType(types.StringType())
