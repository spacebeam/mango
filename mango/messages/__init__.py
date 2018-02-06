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


class BaseResult(models.Model):
    '''
        Base result
    '''
    count = types.IntType()
    page = types.IntType()
    results = compound.ListType(types.StringType())
