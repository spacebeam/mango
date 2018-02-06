# -*- coding: utf-8 -*-
'''
    Mango tasks CRDT's.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import riak
import logging
import ujson as json
from riak.datatypes import Map

'''

uuid = types.UUIDType(default=uuid.uuid4)
account = types.StringType()
name = types.StringType()
description = types.StringType()
payload = types.StringType()
assignees = compound.ListType(types.StringType())
watchers = compound.ListType(types.StringType())
public = types.BooleanType(default=False)
source = types.StringType()
destination = types.StringType()
labels = compound.ListType(types.StringType())
start = types.TimestampType()
acknowledge = types.TimestampType()
stop = types.TimestampType()
deadline = types.TimestampType()
duration = types.StringType()
comments = compound.ListType(types.StringType())
history = compound.ListType(types.StringType())
status = types.StringType(choices=['new',
                                   'now',
                                   'later',
                                   'done'],
                          default='new',
                          required=True)
checked = types.BooleanType(default=False)
checked_by = types.StringType()
checked_at = types.TimestampType(default=arrow.utcnow().timestamp)
created_by = types.StringType()
created_at = types.TimestampType(default=arrow.utcnow().timestamp)
last_update_by = types.StringType()
last_update_at = types.TimestampType()


'''

class TaskMap(object):

    def __init__(
        self,
        client,
        bucket_name,
        bucket_type,
        search_index,
        struct
    ):
        '''
            Task map structure
        '''
        bucket = client.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
        bucket.set_properties({'search_index': search_index})
        self.map = Map(bucket, None)
        # start of map structure
        self.map.registers['uuid'].assign(struct.get('uuid', ''))
        self.map.registers['account'].assign(struct.get('account', ''))
        self.map.registers['name'].assign(struct.get('title', ''))
        self.map.registers['description'].assign(struct.get('description', ''))
        self.map.registers['payload'].assign(struct.get('payload', ''))
        self.map.registers['assignees'].assign(struct.get('assignees', ''))
        self.map.registers['watchers'].assign(struct.get('watchers', ''))
        self.map.registers['public'].assign(struct.get('public', ''))
        self.map.registers['source '].assign(struct.get('source', ''))
        self.map.registers['destination'].assign(struct.get('destination', ''))
        self.map.registers['labels'].assign(struct.get('labels'))
        self.map.registers['start'].assign(struct.get('start', ''))
        self.map.registers['acknowledge'].assign(struct.get('acknowledge', ''))
        self.map.registers['stop'].assign(struct.get('stop', ''))
        self.map.registers['deadline'].assign(struct.get('deadline', ''))
        self.map.registers['duration'].assign(struct.get('duration', ''))
        self.map.registers['comments'].assign(struct.get('comments', ''))
        self.map.registers['history'].assign(struct.get('history', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['checked'].assign(struct.get('checked', ''))
        self.map.registers['checked_by'].assign(struct.get('checked_by', ''))
        self.map.registers['last_update_by'].assign(struct.get('last_update_by', ''))
        self.map.registers['last_update_at'].assign(struct.get('last_update_at', ''))
        self.map.registers['created_by'].assign(struct.get('created_by', ''))
        self.map.registers['created_at'].assign(struct.get('created_at', ''))

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
            "title": event.registers['title'].value,
            "description": event.registers['description'].value,
            "payload": event.registers['payload'].value,
            "assignees": event.registers['assignees'].value,
            "public": event.registers['public'].value,
            "source ": event.registers['source'].value,
            "destination": event.registers['destination'].value,
            "labels": event.registers['labels'].value,
            "url": event.registers['url'].value,
            "start": event.registers['start'].value,
            "ack": event.registers['ack'].value,
            "stop": event.registers['stop'].value,
            "deadline": event.registers['deadline'].value,
            "duration": event.registers['duration'].value,
            "comments": event.registers['comments'].value,
            "status": event.registers['status'].value,
            "checked": event.registers['checked'].value,
            "checked_by": event.registers['checked_by'].value,
            "last_update_by": event.registers['last_update_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
            "created_by": event.registers['created_by'].value,
            "created_at": event.registers['created_at'].value,
            "last_modified": event.registers['last_modified'].value,
            "checksum": event.registers['checksum'].value,
            "hashs": event.registers['hashs'].value,
            "history": event.registers['history'].value,
            "watchers": event.registers['watchers'].value,
        }
        return json.dumps(struct)

    def to_dict(self):
        event = self.map.reload()
        struct = {
            "uuid": event.registers['uuid'].value,
            "account": event.registers['account'].value,
            "title": event.registers['title'].value,
            "description": event.registers['description'].value,
            "payload": event.registers['payload'].value,
            "assignees": event.registers['assignees'].value,
            "public": event.registers['public'].value,
            "source ": event.registers['source'].value,
            "destination": event.registers['destination'].value,
            "labels": event.registers['labels'].value,
            "url": event.registers['url'].value,
            "start": event.registers['start'].value,
            "ack": event.registers['ack'].value,
            "stop": event.registers['stop'].value,
            "deadline": event.registers['deadline'].value,
            "duration": event.registers['duration'].value,
            "comments": event.registers['comments'].value,
            "status": event.registers['status'].value,
            "checked": event.registers['checked'].value,
            "checked_by": event.registers['checked_by'].value,
            "last_update_by": event.registers['last_update_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
            "created_by": event.registers['created_by'].value,
            "created_at": event.registers['created_at'].value,
            "last_modified": event.registers['last_modified'].value,
            "checksum": event.registers['checksum'].value,
            "hashs": event.registers['hashs'].value,
            "history": event.registers['history'].value,
            "watchers": event.registers['watchers'].value,
        }
        return struct
