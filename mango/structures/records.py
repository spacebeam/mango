# -*- coding: utf-8 -*-
'''
    Mango CRDT records structures.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import riak
import logging
import ujson as json
from riak.datatypes import Map


class RecordMap(object):

    def __init__(
        self,
        client,
        bucket_name,
        bucket_type,
        search_index,
        struct
    ):
        '''
            Record map structure
        '''
        bucket = client.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
        bucket.set_properties({'search_index': search_index})
        self.map = Map(bucket, None)
        # start of map structure
        self.map.registers['uuid'].assign(struct.get('uuid', ''))
        self.map.registers['uniqueid'].assign(struct.get('uniqueid', ''))
        self.map.registers['callerid'].assign(struct.get('callerid', ''))
        self.map.registers['account'].assign(struct.get('account', ''))
        self.map.registers['labels'].assign(struct.get('labels', ''))
        self.map.registers['accountcode'].assign(struct.get('accountcode', ''))
        self.map.registers['queue'].assign(struct.get('queue', ''))
        self.map.registers['assigned'].assign(struct.get('assigned', ''))
        self.map.registers['checked'].assign(struct.get('checked', ''))
        self.map.registers['public'].assign(struct.get('public', ''))
        self.map.registers['source'].assign(struct.get('source', ''))
        self.map.registers['destination'].assign(struct.get('destination', ''))
        self.map.registers['channel'].assign(struct.get('channel', ''))
        self.map.registers['source_channel'].assign(struct.get('source_channel', ''))
        self.map.registers['context'].assign(struct.get('context', ''))
        self.map.registers['destination_context'].assign(struct.get('destination_context', ''))
        self.map.registers['destination_number'].assign(struct.get('destination_number', ''))
        self.map.registers['destination_channel'].assign(struct.get('destination_channel', ''))
        self.map.registers['start'].assign(struct.get('start', ''))
        self.map.registers['answer'].assign(struct.get('answer', ''))
        self.map.registers['end'].assign(struct.get('end', ''))
        self.map.registers['duration'].assign(struct.get('duration', ''))
        self.map.registers['seconds'].assign(struct.get('seconds', ''))
        self.map.registers['minutes'].assign(struct.get('minutes', ''))
        self.map.registers['billsec'].assign(struct.get('billsec', ''))
        self.map.registers['billing'].assign(struct.get('billing', ''))
        self.map.registers['disposition'].assign(struct.get('disposition', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['lastapp'].assign(struct.get('lastapp', ''))
        self.map.registers['lastdata'].assign(struct.get('lastdata', ''))
        self.map.registers['recorded'].assign(struct.get('recorded', ''))
        self.map.registers['record_uri'].assign(struct.get('record_uri', ''))
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
            "uniqueid" event.registers['uniqueid'].value,
            "callerid" event.registers['callerid'].value,
            "account" event.registers['account'].value,
            "labels" event.registers['labels'].value,
            "accountcode" event.registers['accountcode'].value,
            "queue" event.registers['queue'].value,
            "assigned": event.registers['assigned'].value,
            "checked": event.registers['checked'].value,
            "public": event.registers['public'].value,
            "source": event.registers['source'].value,
            "destination": event.registers['destination'].value,
            "channel": event.registers['channel'].value,
            "source_channel": event.registers['source_channel'].value,
            "context": event.registers['context'].value,
            "destination_context": event.registers['destination_context'].value,
            "destination_number": event.registers['destination_number'].value,
            "destination_channel": event.registers['destination_channel'].value,
            "start": event.registers['start'].value,
            "answer": event.registers['answer'].value,
            "end": event.registers['end'].value,
            "duration": event.registers['duration'].value,
            "seconds": event.registers['seconds'].value,
            "minutes": event.registers['minutes'].value,
            "billsec": event.registers['billsec'].value,
            "billing": event.registers['billing'].value,
            "disposition": event.registers['disposition'].value,
            "status": event.registers['status'].value,
            "lastapp": event.registers['lastapp'].value,
            "lastdata": event.registers['lastdata'].value,
            "recorded": event.registers['recorded'].value,
            "record_uri": event.registers['record_uri'].value,
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
            "uniqueid" event.registers['uniqueid'].value,
            "callerid" event.registers['callerid'].value,
            "account" event.registers['account'].value,
            "labels" event.registers['labels'].value,
            "accountcode" event.registers['accountcode'].value,
            "queue" event.registers['queue'].value,
            "assigned": event.registers['assigned'].value,
            "checked": event.registers['checked'].value,
            "public": event.registers['public'].value,
            "source": event.registers['source'].value,
            "destination": event.registers['destination'].value,
            "channel": event.registers['channel'].value,
            "source_channel": event.registers['source_channel'].value,
            "context": event.registers['context'].value,
            "destination_context": event.registers['destination_context'].value,
            "destination_number": event.registers['destination_number'].value,
            "destination_channel": event.registers['destination_channel'].value,
            "start": event.registers['start'].value,
            "answer": event.registers['answer'].value,
            "end": event.registers['end'].value,
            "duration": event.registers['duration'].value,
            "seconds": event.registers['seconds'].value,
            "minutes": event.registers['minutes'].value,
            "billsec": event.registers['billsec'].value,
            "billing": event.registers['billing'].value,
            "disposition": event.registers['disposition'].value,
            "status": event.registers['status'].value,
            "lastapp": event.registers['lastapp'].value,
            "lastdata": event.registers['lastdata'].value,
            "recorded": event.registers['recorded'].value,
            "record_uri": event.registers['record_uri'].value,
            "checked": event.registers['checked'].value,
            "checked_by":event.registers['checked_by'].value,
            "created_at": event.registers['created_at'].value,
            "updated_by": event.registers['updated_by'].value,
            "updated_at": event.registers['updated_at'].value,
            "uri": event.registers['uri'].value,
        }
        return struct