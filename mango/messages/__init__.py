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
    leads = compound.ModelType(SimpleResource)
    tasks = compound.ModelType(SimpleResource)
    sms = compound.ModelType(SimpleResource)
    comments = compound.ModelType(SimpleResource)
    queries = compound.ModelType(SimpleResource)
    secrets = compound.ModelType(SimpleResource)
    emails = compound.ModelType(SimpleResource)
    calls = compound.ModelType(SimpleResource)
    contacts = compound.ModelType(SimpleResource)
    dids = compound.ModelType(SimpleResource)
    extens = compound.ModelType(SimpleResource)
    ivrs = compound.ModelType(SimpleResource)
    queues = compound.ModelType(SimpleResource)
    campaigns = compound.ModelType(SimpleResource)
    nodes = compound.ModelType(SimpleResource)
    units = compound.ModelType(SimpleResource)
    kmeans = compound.ModelType(SimpleResource)
    stochastics = compound.ModelType(SimpleResource)
    apps = compound.ModelType(SimpleResource)
    images = compound.ModelType(SimpleResource)
    sounds = compound.ModelType(SimpleResource)
    indexes = compound.ModelType(SimpleResource)
    hashes = compound.ModelType(SimpleResource)
    leagues = compound.ModelType(SimpleResource)
    reports = compound.ModelType(SimpleResource)
    upgrades = compound.ModelType(SimpleResource)
    currencies = compound.ModelType(SimpleResource)
    payments = compound.ModelType(SimpleResource)
    fire = compound.ModelType(SimpleResource)

class BaseResult(models.Model):
    '''
        Base result
    '''
    count = types.IntType()
    page = types.IntType()
    results = compound.ListType(types.StringType())