# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import uuid as _uuid
from schematics import models
from schematics import types
from schematics.types import compound
from mango.messages import tasks


class SimpleResource(models.Model):
    '''
        Simple Resource
    '''
    contains = compound.ListType(types.UUIDType())
    total = types.IntType()


class Resource(models.Model):
    ''' 
        Resource
    '''
    records = compound.ModelType(SimpleResource)
    tasks = compound.ModelType(SimpleResource)
    addresses = compound.ModelType(SimpleResource)
    total = types.IntType()


class BaseResult(models.Model):
    '''
        Base result
    '''
    count = types.IntType()
    page = types.IntType()
    results = compound.ListType(types.StringType())
    #results = compound.ListType(compound.ModelType(records.Record))


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