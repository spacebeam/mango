# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Space Beam LLC'


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
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['role'].assign(struct.get('role', ''))
        self.map.registers['account'].assign(struct.get('account', ''))
        self.map.registers['account_type'].assign(struct.get('account_type', ''))
        self.map.registers['name'].assign(struct.get('name', ''))
        self.map.registers['description'].assign(struct.get('description', ''))
        self.map.registers['nickname'].assign(struct.get('nickname', ''))
        self.map.registers['first_name'].assign(struct.get('first_name', ''))
        self.map.registers['last_name'].assign(struct.get('last_name', ''))
        self.map.registers['middle_name'].assign(struct.get('middle_name', ''))
        self.map.registers['password'].assign(struct.get('password', ''))
        self.map.registers['email'].assign(struct.get('email', ''))
        self.map.registers['phone_number'].assign(struct.get('phone_number', ''))
        self.map.registers['extension'].assign(struct.get('extension', ''))
        self.map.registers['country_code'].assign(struct.get('country_code', ''))
        self.map.registers['timezone'].assign(struct.get('timezone', ''))
        self.map.registers['company'].assign(struct.get('company', ''))
        self.map.registers['location'].assign(struct.get('location', ''))
        self.map.registers['phones'].assign(struct.get('phones', ''))
        self.map.registers['emails'].assign(struct.get('emails', ''))
        self.map.registers['history'].assign(struct.get('history', ''))
        self.map.registers['labels'].assign(struct.get('labels'))
        self.map.registers['orgs'].assign(struct.get('orgs', ''))
        self.map.registers['teams'].assign(struct.get('teams', ''))
        self.map.registers['members'].assign(struct.get('members', ''))
        self.map.registers['checked'].assign(struct.get('checked', ''))
        self.map.registers['checked_by'].assign(struct.get('checked_by', ''))
        self.map.registers['checked_at'].assign(struct.get('checked_at', ''))
        self.map.registers['created_by'].assign(struct.get('created_by', ''))
        self.map.registers['created_at'].assign(struct.get('created_at', ''))
        self.map.registers['last_update_at'].assign(struct.get('last_update_at', ''))
        self.map.registers['last_update_by'].assign(struct.get('last_update_by', ''))
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
            "status": event.registers['status'].value,
            "role": event.registers['role'].value,
            "account": event.registers['account'].value,
            "account_type": event.registers['account_type'].value,
            "name": event.registers['name'].value,
            "description": event.registers['description'].value,
            "nickname": event.registers['nickname'].value,
            "first_name": event.registers['first_name'].value,
            "last_name": event.registers['last_name'].value,
            "middle_name": event.registers['middle_name'].value,
            "password": event.registers['password'].value,
            "email": event.registers['email'].value,
            "phone_number": event.registers['phone_number'].value,
            "extension": event.registers['extension'].value,
            "country_code": event.registers['country_code'].value,
            "timezone": event.registers['timezone'].value,
            "company": event.registers['company'].value,
            "location": event.registers['location'].value,
            "phones": event.registers['phones'].value,
            "emails": event.registers['emails'].value,
            "history": event.registers['history'].value,
            "labels": event.registers['labels'].value,
            "orgs": event.registers['orgs'].value,
            "teams": event.registers['teams'].value,
            "members": event.registers['members'].value,
            "checked": event.registers['checked'].value,
            "checked_at": event.registers['checked_at'].value,
            "checked_by": event.registers['checked_by'].value,
            "created_at": event.registers['created_at'].value,
            "created_by": event.registers['created_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
            "last_update_by": event.registers['last_update_by'].value,
        }
        return json.dumps(struct)

    def to_dict(self):
        event = self.map.reload()
        struct = {
            "uuid": event.registers['uuid'].value,
            "status": event.registers['status'].value,
            "account": event.registers['account'].value,
            "role": event.registers['role'].value,
            "account_type": event.registers['account_type'].value,
            "name": event.registers['name'].value,
            "description": event.registers['description'].value,
            "nickname": event.registers['nickname'].value,
            "first_name": event.registers['first_name'].value,
            "last_name": event.registers['last_name'].value,
            "middle_name": event.registers['middle_name'].value,
            "password": event.registers['password'].value,
            "email": event.registers['email'].value,
            "phone_number": event.registers['phone_number'].value,
            "extension": event.registers['extension'].value,
            "country_code": event.registers['country_code'].value,
            "timezone": event.registers['timezone'].value,
            "company": event.registers['company'].value,
            "location": event.registers['location'].value,
            "phones": event.registers['phones'].value,
            "emails": event.registers['emails'].value,
            "history": event.registers['history'].value,
            "labels": event.registers['labels'].value,
            "orgs": event.registers['orgs'].value,
            "teams": event.registers['teams'].value,
            "members": event.registers['members'].value,
            "checked": event.registers['checked'].value,
            "checked_at": event.registers['checked_at'].value,
            "checked_by": event.registers['checked_by'].value,
            "created_at": event.registers['created_at'].value,
            "created_by": event.registers['created_by'].value,
            "last_update_at": event.registers['last_update_at'].value,
            "last_update_by": event.registers['last_update_by'].value,
        }
        return struct
