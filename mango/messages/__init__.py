# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


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
    # apps = compound.ModelType(SimpleResource)
    # calls = compound.ModelType(SimpleResource)
    # queues = compound.ModelType(SimpleResource)
    records = compound.ModelType(SimpleResource)

    total = types.IntType()