# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import uuid
import uuid as _id

from schematics import models
from schematics import types
from schematics.types import compound

from mango.messages import tasks
from mango.messages import records


class BaseResult(models.Model):
    '''
        base result
    '''
    count = types.IntType()
    page = types.IntType()


class SimpleResource(models.Model):
    '''
        Simple resource
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
        base result
    '''
    count = types.IntType()
    page = types.IntType()
    results = compound.ListType(compound.ModelType(records.Record))


class BaseHistory(models.Model):
    '''
        base history

        Scopes: accounts, numbers
    '''
    uuid = types.UUIDType(default=_id.uuid4)
    record_uuid = types.UUIDType(default=_id.uuid4)
    ban =  types.UUIDType(default=_id.uuid4) # 'billing account number'
    country_number = types.IntType()
    number = types.StringType()
    campaign_uuid = types.UUIDType(default=_id.uuid4)
    start_time = types.DateTimeType()
    caller_id = types.StringType()
    caller_id_name = types.StringType()
    origin_number = types.StringType()
    origin_city = types.StringType()
    origin_state = types.StringType()
    origin_province = types.StringType()
    destination_type = types.IntType()
    destination_contry_code = types.StringType()
    destination_number = types.StringType()
    destination_city = types.StringType()
    destination_state = types.StringType()
    duration = types.IntType()
    duration_unrounded = types.IntType()
    cost = types.IntType()
    special_rate = types.IntType()
    lead_type = types.IntType()
    web_call = types.BooleanType(default=False)


class ConectedDuration(models.Model):
    '''
        connected duration
    '''
    uuid = types.UUIDType(default=_id.uuid4)
    customer_uuid = types.UUIDType(default=_id.uuid4)
    phone_1 = types.StringType()
    first_name = types.StringType()
    rep_phone = types.StringType()
    keyword = types.StringType()
    duration_unrounded = types.IntType()
    record_uuid = types.UUIDType(default=_id.uuid4)


class VoiceCall(models.Model):
    '''
        voice call
    '''
    uuid = types.UUIDType(default=_id.uuid4)
    account_uuid = types.UUIDType(default=_id.uuid4)
    phone_1 = types.StringType()
    first_name = types.StringType()
    last_name = types.StringType()
    rep_phone = types.StringType()
    keyword = types.StringType()