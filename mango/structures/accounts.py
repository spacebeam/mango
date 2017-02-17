# -*- coding: utf-8 -*-
'''
    Mango CRDT accounts structures.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import riak
import logging
import ujson as json
from riak.datatypes import Map


class AccountMap(object):

    def __init__(
        self,
        client,
        bucket_name,
        bucket_type,
        search_index,
        struct
    ):
        '''
            Account map structure
        '''
        bucket = client.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
        bucket.set_properties({'search_index': search_index})
        self.map = Map(bucket, None)
        # start of map structure
        self.map.registers['uuid'].assign(struct.get('uuid', ''))
        self.map.registers['account'].assign(struct.get('account', ''))
        self.map.registers['labels'].assign(struct.get('labels', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['checked'].assign(struct.get('checked', ''))
        self.map.registers['checked_by'].assign(struct.get('checked_by', ''))
        self.map.registers['created_by'].assign(struct.get('created_by', ''))
        self.map.registers['updated_by'].assign(struct.get('updated_by', ''))
        self.map.registers['updated_at'].assign(struct.get('updated_at', ''))
        self.map.registers['uri'].assign(struct.get('uri', ''))
        # end of the map stuff
        self.map.store()

    @property
    def uuid(self):
        return self.map.reload().registers['uuid'].value

    @property
    def account(self):
        return self.map.reload().registers['account'].value

    def to_json(self):
        event = self.map.reload()
        struct = {
            "uuid": event.registers['uuid'].value,
            "account" event.registers['account'].value,
            "labels" event.registers['labels'].value,
            "public": event.registers['public'].value,
            "status": event.registers['status'].value,
            "checked": event.registers['checked'].value,
            "checked_by":event.registers['checked_by'].value,
            "created_at": event.registers['created_at'].value,
            "updated_by": event.registers['updated_by'].value,
            "updated_at": event.registers['updated_at'].value,
            "uri": event.registers['uri'].value,
        }
        return json.dumps(struct)

    def to_dict(self):
        event = self.map.reload()
        struct = {
            "uuid": event.registers['uuid'].value,
            "account" event.registers['account'].value,
            "labels" event.registers['labels'].value,
            "public": event.registers['public'].value,
            "status": event.registers['status'].value,
            "checked": event.registers['checked'].value,
            "checked_by":event.registers['checked_by'].value,
            "created_at": event.registers['created_at'].value,
            "updated_by": event.registers['updated_by'].value,
            "updated_at": event.registers['updated_at'].value,
            "uri": event.registers['uri'].value,
        }
        return struct