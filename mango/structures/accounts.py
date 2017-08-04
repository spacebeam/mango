# -*- coding: utf-8 -*-
'''
    Starfruit queues CRDT's.
'''

# This file is part of starfruit.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__authors__ = 'Team Machine'


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
            Accounts event from your white-headed capuchins.
        '''
        bucket = client.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
        bucket.set_properties({'search_index': search_index})

        # now we define or map data structure
        self.map = Map(bucket, None)
        self.map.registers['uuid'].assign(struct.get('uuid', ''))
        self.map.registers['account'].assign(struct.get('account', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['created_at'].assign(struct.get('created_at', ''))
        self.map.registers['created_by'].assign(struct.get('created_by', ''))
        self.map.registers['updated_by'].assign(struct.get('updated_by', ''))
        self.map.registers['updated_at'].assign(struct.get('updated_at', ''))
        self.map.registers['change_history '].assign(struct.get('change_history', ''))
        self.map.registers['tags'].assign(struct.get('tags', ''))
        self.map.registers['snapshots'].assign(struct.get('snapshots', ''))
        self.map.registers['addresses'].assign(struct.get('addresses', ''))
        # and finally we store or CRDT datatype inside our database
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
            "uuid":event.registers['uuid'].value,
            "account":event.registers['account'].value,
            "status":event.registers['status'].value,
            "created_at":event.registers['created_at'].value,
            "created_by":event.registers['created_by'].value,
            "updated_by":event.registers['updated_by'].value,
            "updated_at":event.registers['updated_at'].value,
            "change_history ":event.registers['change_history'].value,
            "tags":event.registers['tags'].value,
            "snapshots":event.registers['snapshots'].value,
            "addresses":event.registers['addresses'].value,
        }
        return json.dumps(struct)

    def to_dict(self):
        event = self.map.reload()
        struct = {
            "uuid":event.registers['uuid'].value,
            "account":event.registers['account'].value,
            "status":event.registers['status'].value,
            "created_at":event.registers['created_at'].value,
            "created_by":event.registers['created_by'].value,
            "updated_by":event.registers['updated_by'].value,
            "updated_at":event.registers['updated_at'].value,
            "change_history ":event.registers['change_history'].value,
            "tags":event.registers['tags'].value,
            "snapshots":event.registers['snapshots'].value,
            "addresses":event.registers['addresses'].value,
        }
        return struct