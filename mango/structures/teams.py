# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Team Machine'


import riak
import logging
import ujson as json
from riak.datatypes import Map


class TeamMap(object):

    def __init__(
        self,
        client,
        bucket_name,
        bucket_type,
        search_index,
        struct
    ):
        '''
            Team map structure
        '''
        bucket = client.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
        bucket.set_properties({'search_index': search_index})
        self.map = Map(bucket, None)
        # start of map structure
        self.map.registers['uuid'].assign(struct.get('uuid', ''))
        self.map.registers['account'].assign(struct.get('account', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['name'].assign(struct.get('name', ''))
        self.map.registers['description'].assign(struct.get('description', ''))
        self.map.registers['resources'].assign(struct.get('resources', ''))
        self.map.registers['permissions'].assign(struct.get('permissions', ''))
        self.map.registers['members'].assign(struct.get('members', ''))
        self.map.registers['labels'].assign(struct.get('labels'))
        self.map.registers['history'].assign(struct.get('history', ''))
        self.map.registers['checked'].assign(struct.get('checked', ''))
        self.map.registers['checked_by'].assign(struct.get('checked_by', ''))
        self.map.registers['checked_at'].assign(struct.get('checked_at', ''))
        self.map.registers['created_by'].assign(struct.get('created_by', ''))
        self.map.registers['created_at'].assign(struct.get('created_at', ''))
        self.map.registers['last_update_by'].assign(struct.get('last_update_by', ''))
        self.map.registers['last_update_at'].assign(struct.get('last_update_at', ''))
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
            "account": event.registers['account'].value,
            "status": event.registers['status'].value,
            "name": event.registers['name'].value,
            "description": event.registers['description'].value,
            "resources": event.registers['resources'].value,
            "permissions": event.registers['permissions'].value,
            "members": event.registers['members'].value,
            "labels": event.registers['labels'].value,
            "history": event.registers['history'].value,
            "checked": event.registers['checked'].value,
            "checked_by": event.registers['checked_by'].value,
            "checked_at": event.registers['checked_at'].value,
            "created_by": event.registers['created_by'].value,
            "created_at": event.registers['created_at'].value,
            "last_update_by": event.registers['last_update_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
        }
        return json.dumps(struct)

    def to_dict(self):
        event = self.map.reload()
        struct = {
            "uuid": event.registers['uuid'].value,
            "account": event.registers['account'].value,
            "status": event.registers['status'].value,
            "name": event.registers['name'].value,
            "description": event.registers['description'].value,
            "resources": event.registers['resources'].value,
            "permissions": event.registers['permissions'].value,
            "members": event.registers['members'].value,
            "labels": event.registers['labels'].value,
            "history": event.registers['history'].value,
            "checked": event.registers['checked'].value,
            "checked_by": event.registers['checked_by'].value,
            "checked_at": event.registers['checked_at'].value,
            "created_by": event.registers['created_by'].value,
            "created_at": event.registers['created_at'].value,
            "last_update_by": event.registers['last_update_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
        }
        return struct
