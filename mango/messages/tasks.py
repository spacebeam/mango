# -*- coding: utf-8 -*-
'''
    Mango tasks models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import arrow
import uuid

from schematics import models
from schematics import types


# missing compoing of comments on task history


class Task(models.Model):
    '''
        Task Object Data Structure
    '''
    uuid = types.UUIDType(default=uuid.uuid4)

    title = types.StringType()

    first_name = types.StringType()
    last_name = types.StringType()
    description = types.StringType()
    
    label = types.StringType()
    
    category = types.StringType()

    email = types.StringType()
    
    account = types.StringType()
    accountcode = types.StringType()
    userfield = types.StringType()
    
    assigned = types.BooleanType(default=False)
    checked = types.BooleanType(default=False)

    public = types.BooleanType(default=False)

    source = types.StringType()
    destination = types.StringType()
    
    channel = types.StringType()
    source_channel = types.StringType()
    
    context = types.StringType()
    
    destination_context = types.StringType()

    destination_number = types.StringType()
    
   
    destination_channel = types.StringType()
    
    start = types.DateTimeType()
    answer = types.DateTimeType()
    end = types.DateTimeType()

    duration = types.IntType()
    billsec = types.IntType()
    billing = types.IntType()
    rate = types.IntType()

    disposition = types.StringType()
    status = types.StringType(choices=['now',
                                       'later',
                                       'done'],
                              default='now',
                              required=True)
    
    priority = types.StringType(choices=['small',
                                       'medium',
                                       'hight'],
                              default='small',
                              required=True)
    
    severity = types.StringType(choices=['info',
                                       'warning',
                                       'error'],
                              default='info',
                              required=True)


    checked = types.BooleanType(default=False)
    checked_by = types.StringType()
    
    created = types.DateTimeType(default=arrow.utcnow().naive)

    last_modified = types.DateTimeType()
    updated_by = types.StringType()
    updated_at = types.DateTimeType()

    uri = types.StringType()