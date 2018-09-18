# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Space Beam LLC'


import riak
import logging
import ujson as json
from riak.datatypes import Map


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
        self.map.registers['subject'].assign(struct.get('subject', ''))
        self.map.registers['description'].assign(struct.get('description', ''))
        self.map.registers['data'].assign(struct.get('data', ''))
        self.map.registers['assign'].assign(struct.get('assign', ''))
        self.map.registers['public'].assign(struct.get('public', ''))
        self.map.registers['source '].assign(struct.get('source', ''))
        self.map.registers['destination'].assign(struct.get('destination', ''))
        self.map.registers['labels'].assign(struct.get('labels'))
        self.map.registers['start_time'].assign(struct.get('start_time', ''))
        self.map.registers['ack_time'].assign(struct.get('ack_time', ''))
        self.map.registers['stop_time'].assign(struct.get('stop_time', ''))
        self.map.registers['deadline'].assign(struct.get('deadline', ''))
        self.map.registers['duration'].assign(struct.get('duration', ''))
        self.map.registers['comments'].assign(struct.get('comments', ''))
        self.map.registers['history'].assign(struct.get('history', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
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
            "subject": event.registers['subject'].value,
            "description": event.registers['description'].value,
            "data": event.registers['data'].value,
            "assign": event.registers['assign'].value,
            "public": event.registers['public'].value,
            "source ": event.registers['source'].value,
            "destination": event.registers['destination'].value,
            "labels": event.registers['labels'].value,
            "start_time": event.registers['start_time'].value,
            "ack_time": event.registers['ack_time'].value,
            "stop_time": event.registers['stop_time'].value,
            "deadline": event.registers['deadline'].value,
            "duration": event.registers['duration'].value,
            "comments": event.registers['comments'].value,
            "history": event.registers['history'].value,
            "status": event.registers['status'].value,
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
            "subject": event.registers['subject'].value,
            "description": event.registers['description'].value,
            "data": event.registers['data'].value,
            "assign": event.registers['assign'].value,
            "public": event.registers['public'].value,
            "source ": event.registers['source'].value,
            "destination": event.registers['destination'].value,
            "labels": event.registers['labels'].value,
            "start_time": event.registers['start_time'].value,
            "ack_time": event.registers['ack_time'].value,
            "stop_time": event.registers['stop_time'].value,
            "deadline": event.registers['deadline'].value,
            "duration": event.registers['duration'].value,
            "comments": event.registers['comments'].value,
            "history": event.registers['history'].value,
            "status": event.registers['status'].value,
            "checked": event.registers['checked'].value,
            "checked_by": event.registers['checked_by'].value,
            "checked_at": event.registers['checked_at'].value,
            "created_by": event.registers['created_by'].value,
            "created_at": event.registers['created_at'].value,
            "last_update_by": event.registers['last_update_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
        }
        return struct
