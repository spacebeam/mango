# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


from schematics import models
from schematics import types
from schematics.types import compound


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
    sms = compound.ModelType(SimpleResource)
    emails = compound.ModelType(SimpleResource)
    sounds = compound.ModelType(SimpleResource)
    units = compound.ModelType(SimpleResource)
    nodes = compound.ModelType(SimpleResource)
    clusters = compound.ModelType(SimpleResource) 
    models = compound.ModelType(SimpleResource)
    images = compound.ModelType(SimpleResource)
    secrets = compound.ModelType(SimpleResource)
    queries = compound.ModelType(SimpleResource)
    ivrs = compound.ModelType(SimpleResource)
    extens = compound.ModelType(SimpleResource)
    users = compound.ModelType(SimpleResource)
    events = compound.ModelType(SimpleResource)
    tasks = compound.ModelType(SimpleResource)
    orgs = compound.ModelType(SimpleResource)
    contacts = compound.ModelType(SimpleResource)
    campaigns = compound.ModelType(SimpleResource)
    dids = compound.ModelType(SimpleResource)
    comments = compound.ModelType(SimpleResource)


class BaseResult(models.Model):
    '''
        Base result
    '''
    count = types.IntType()
    page = types.IntType()
    results = compound.ListType(types.StringType())