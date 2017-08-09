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
        self.map.registers['name'].assign(struct.get('name', ''))
        self.map.registers['permission'].assign(struct.get('permission', ''))
        self.map.registers['members'].assign(struct.get('members', ''))
        self.map.registers['resources'].assign(struct.get('resources', ''))
        self.map.registers['created_by'].assign(struct.get('created_by', ''))
        self.map.registers['created_at'].assign(struct.get('created_at', ''))
        self.map.registers['updated_by'].assign(struct.get('updated_by', ''))
        self.map.registers['updated_at'].assign(struct.get('updated_at', ''))
        self.map.registers['change_history'].assign(struct.get('change_history', ''))
        self.map.registers['labels'].assign(struct.get('labels', ''))
        self.map.registers['snapshots'].assign(struct.get('snapshots', ''))
        self.map.registers['addresses'].assign(struct.get('addresses', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['leads'].assign(struct.get('leads', ''))
        self.map.registers['tasks'].assign(struct.get('tasks', ''))
        self.map.registers['sms'].assign(struct.get('sms', ''))
        self.map.registers['comments'].assign(struct.get('comments', ''))
        self.map.registers['queries'].assign(struct.get('queries', ''))
        self.map.registers['secrets'].assign(struct.get('secrets', ''))
        self.map.registers['emails'].assign(struct.get('emails', ''))
        self.map.registers['calls'].assign(struct.get('calls', ''))
        self.map.registers['contacts'].assign(struct.get('contacts', ''))
        self.map.registers['dids'].assign(struct.get('dids', ''))
        self.map.registers['extens'].assign(struct.get('extens', ''))
        self.map.registers['ivrs'].assign(struct.get('ivrs', ''))
        self.map.registers['queues'].assign(struct.get('queues', ''))
        self.map.registers['campaigns'].assign(struct.get('campaigns', ''))
        self.map.registers['nodes'].assign(struct.get('nodes', ''))
        self.map.registers['units'].assign(struct.get('units', ''))
        self.map.registers['kmeans'].assign(struct.get('kmeans', ''))
        self.map.registers['stochastics'].assign(struct.get('stochastics', ''))
        self.map.registers['apps'].assign(struct.get('apps', ''))
        self.map.registers['images'].assign(struct.get('images', ''))
        self.map.registers['sounds'].assign(struct.get('sounds', ''))
        self.map.registers['indexes'].assign(struct.get('indexes', ''))
        self.map.registers['hashes'].assign(struct.get('hashes', ''))
        self.map.registers['leagues'].assign(struct.get('leagues', ''))
        self.map.registers['reports'].assign(struct.get('reports', ''))
        self.map.registers['upgrades'].assign(struct.get('upgrades', ''))
        self.map.registers['currencies'].assign(struct.get('currencies', ''))
        self.map.registers['payments'].assign(struct.get('payments', ''))
        self.map.registers['fire'].assign(struct.get('fire', ''))
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
            "name": event.registers['name'].value,
            "permission": event.registers['permission'].value,
            "members": event.registers['members'].value,
            "resources": event.registers['resources'].value,
            "created_by": event.registers['created_by'].value,
            "created_at": event.registers['created_at'].value,
            "updated_by": event.registers['updated_by'].value,
            "updated_at": event.registers['updated_at'].value,
            "change_history": event.registers['change_history'].value,
            "labels": event.registers['labels'].value,
            "snapshots": event.registers['snapshots'].value,
            "addresses": event.registers['addresses'].value,
            "status": event.registers['status'].value,
            "leads": event.registers['leads'].value,
            "tasks": event.registers['tasks'].value,
            "sms": event.registers['sms'].value,
            "comments": event.registers['comments'].value,
            "queries": event.registers['queries'].value,
            "secrets": event.registers['secrets'].value,
            "emails": event.registers['emails'].value,
            "calls": event.registers['calls'].value,
            "contacts": event.registers['contacts'].value,
            "dids": event.registers['dids'].value,
            "extens": event.registers['extens'].value,
            "ivrs": event.registers['ivrs'].value,
            "queues": event.registers['queues'].value,
            "campaigns": event.registers['campaigns'].value,
            "nodes": event.registers['nodes'].value,
            "units": event.registers['units'].value,
            "kmeans": event.registers['kmeans'].value,
            "stochastics": event.registers['stochastics'].value,
            "apps": event.registers['apps'].value,
            "images": event.registers['images'].value,
            "sounds": event.registers['sounds'].value,
            "indexes": event.registers['indexes'].value,
            "hashes": event.registers['hashes'].value,
            "leagues": event.registers['leagues'].value,
            "reports": event.registers['reports'].value,
            "upgrades": event.registers['upgrades'].value,
            "currencies": event.registers['currencies'].value,
            "payments": event.registers['payments'].value,
            "fire": event.registers['fire'].value,
        }
        return json.dumps(struct)

    def to_dict(self):
        event = self.map.reload()
        struct = {
            "uuid": event.registers['uuid'].value,
            "account": event.registers['account'].value,
            "name": event.registers['name'].value,
            "permission": event.registers['permission'].value,
            "members": event.registers['members'].value,
            "resources": event.registers['resources'].value,
            "created_by": event.registers['created_by'].value,
            "created_at": event.registers['created_at'].value,
            "updated_by": event.registers['updated_by'].value,
            "updated_at": event.registers['updated_at'].value,
            "change_history": event.registers['change_history'].value,
            "labels": event.registers['labels'].value,
            "snapshots": event.registers['snapshots'].value,
            "addresses": event.registers['addresses'].value,
            "status": event.registers['status'].value,
            "leads": event.registers['leads'].value,
            "tasks": event.registers['tasks'].value,
            "sms": event.registers['sms'].value,
            "comments": event.registers['comments'].value,
            "queries": event.registers['queries'].value,
            "secrets": event.registers['secrets'].value,
            "emails": event.registers['emails'].value,
            "calls": event.registers['calls'].value,
            "contacts": event.registers['contacts'].value,
            "dids": event.registers['dids'].value,
            "extens": event.registers['extens'].value,
            "ivrs": event.registers['ivrs'].value,
            "queues": event.registers['queues'].value,
            "campaigns": event.registers['campaigns'].value,
            "nodes": event.registers['nodes'].value,
            "units": event.registers['units'].value,
            "kmeans": event.registers['kmeans'].value,
            "stochastics": event.registers['stochastics'].value,
            "apps": event.registers['apps'].value,
            "images": event.registers['images'].value,
            "sounds": event.registers['sounds'].value,
            "indexes": event.registers['indexes'].value,
            "hashes": event.registers['hashes'].value,
            "leagues": event.registers['leagues'].value,
            "reports": event.registers['reports'].value,
            "upgrades": event.registers['upgrades'].value,
            "currencies": event.registers['currencies'].value,
            "payments": event.registers['payments'].value,
            "fire": event.registers['fire'].value,
        }
        return struct