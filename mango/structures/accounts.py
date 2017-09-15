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
            Account map structure
        '''
        bucket = client.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
        bucket.set_properties({'search_index': search_index})
        self.map = Map(bucket, None)
        # start of map structure
        self.map.registers['uuid'].assign(struct.get('uuid', ''))
        self.map.registers['account'].assign(struct.get('account', ''))
        self.map.registers['first_name'].assign(struct.get('first_name', ''))
        self.map.registers['last_name'].assign(struct.get('last_name', ''))
        self.map.registers['type'].assign(struct.get('type', ''))
        self.map.registers['account_type'].assign(struct.get('account_type', ''))
        self.map.registers['permission'].assign(struct.get('permission', ''))
        self.map.registers['orgs'].assign(struct.get('orgs', ''))
        self.map.registers['password'].assign(struct.get('password', ''))
        self.map.registers['members'].assign(struct.get('members', ''))
        self.map.registers['teams'].assign(struct.get('teams', ''))
        self.map.registers['labels'].assign(struct.get('labels', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['email'].assign(struct.get('email', ''))
        self.map.registers['phone_number'].assign(struct.get('phone_number', ''))
        self.map.registers['extension'].assign(struct.get('extension', ''))
        self.map.registers['country_code'].assign(struct.get('country_code', ''))
        self.map.registers['timezone'].assign(struct.get('timezone', ''))
        self.map.registers['company'].assign(struct.get('company', ''))
        self.map.registers['location'].assign(struct.get('location', ''))
        self.map.registers['membership'].assign(struct.get('membership', ''))
        self.map.registers['resources'].assign(struct.get('resources', ''))
        self.map.registers['phones'].assign(struct.get('phones', ''))
        self.map.registers['emails'].assign(struct.get('emails', ''))
        self.map.registers['max_channels'].assign(struct.get('max_channels', ''))
        self.map.registers['is_admin'].assign(struct.get('is_admin', ''))
        self.map.registers['checked'].assign(struct.get('checked', ''))
        self.map.registers['checked_by'].assign(struct.get('checked_by', ''))
        self.map.registers['last_update_by'].assign(struct.get('last_update_by', ''))
        self.map.registers['last_update_at'].assign(struct.get('last_update_at', ''))
        self.map.registers['created_at'].assign(struct.get('created_at', ''))
        self.map.registers['login_at'].assign(struct.get('login_at', ''))
        self.map.registers['logout_at'].assign(struct.get('logout_at', ''))
        self.map.registers['uri'].assign(struct.get('uri', ''))
        self.map.registers['layout'].assign(struct.get('layout', ''))
        self.map.registers['powerdailer'].assign(struct.get('powerdailer', ''))
        self.map.registers['lead_access'].assign(struct.get('lead_access', ''))
        self.map.registers['phone_server'].assign(struct.get('phone_server', ''))
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
            "first_name": event.registers['first_name'].value,
            "last_name": event.registers['last_name'].value,
            "type": event.registers['type'].value,
            "account_type": event.registers['account_type'].value,
            "permission": event.registers['permission'].value,
            "orgs": event.registers['orgs'].value,
            "password": event.registers['password'].value,
            "members": event.registers['members'].value,
            "teams": event.registers['teams'].value,
            "labels": event.registers['labels'].value, 
            "status": event.registers['status'].value,
            "email": event.registers['email'].value,
            "phone_number": event.registers['phone_number'].value,
            "extension": event.registers['extension'].value,
            "country_code": event.registers['country_code'].value,
            "timezone": event.registers['timezone'].value,
            "company": event.registers['company'].value,
            "location": event.registers['location'].value,
            "membership": event.registers['membership'].value,
            "resources": event.registers['resources'].value,
            "phones": event.registers['phones'].value,
            "emails": event.registers['emails'].value,
            "max_channels": event.registers['max_channels'].value,
            "is_admin": event.registers['is_admin'].value,
            "checked": event.registers['checked'].value,
            "checked_by": event.registers['checked_by'].value,
            "last_update_by": event.registers['last_update_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
            "created_at": event.registers['created_at'].value,
            "login_at": event.registers['login_at'].value,
            "logout_at": event.registers['logout_at'].value,
            "uri": event.registers['uri'].value,
            "layout": event.registers['layout'].value,
            "powerdailer": event.registers['powerdailer'].value,
            "lead_access": event.registers['lead_access'].value,
            "phone_server": event.registers['phone_server'].value,
        }
        return json.dumps(struct)

    def to_dict(self):
        event = self.map.reload()
        struct = {
            "uuid": event.registers['uuid'].value,
            "account": event.registers['account'].value,
            "first_name": event.registers['first_name'].value,
            "last_name": event.registers['last_name'].value,
            "type": event.registers['type'].value,
            "account_type": event.registers['account_type'].value,
            "permission": event.registers['permission'].value,
            "orgs": event.registers['orgs'].value,
            "password": event.registers['password'].value,
            "members": event.registers['members'].value,
            "teams": event.registers['teams'].value,
            "labels": event.registers['labels'].value, 
            "status": event.registers['status'].value,
            "email": event.registers['email'].value,
            "phone_number": event.registers['phone_number'].value,
            "extension": event.registers['extension'].value,
            "country_code": event.registers['country_code'].value,
            "timezone": event.registers['timezone'].value,
            "company": event.registers['company'].value,
            "location": event.registers['location'].value,
            "membership": event.registers['membership'].value,
            "resources": event.registers['resources'].value,
            "phones": event.registers['phones'].value,
            "emails": event.registers['emails'].value,
            "max_channels": event.registers['max_channels'].value,
            "is_admin": event.registers['is_admin'].value,
            "checked": event.registers['checked'].value,
            "checked_by": event.registers['checked_by'].value,
            "last_update_by": event.registers['last_update_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
            "created_at": event.registers['created_at'].value,
            "login_at": event.registers['login_at'].value,
            "logout_at": event.registers['logout_at'].value,
            "uri": event.registers['uri'].value,
            "layout": event.registers['layout'].value,
            "powerdailer": event.registers['powerdailer'].value,
            "lead_access": event.registers['lead_access'].value,
            "phone_server": event.registers['phone_server'].value,
        }
        return struct