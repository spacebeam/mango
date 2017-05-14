# -*- coding: utf-8 -*-
'''
    Mango tasks CRDT's structures.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


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
        self.map.registers['title'].assign(struct.get('title', ''))
        self.map.registers['description'].assign(struct.get('description', ''))
        self.map.registers['payload'].assign(struct.get('payload', ''))
        self.map.registers['assignees'].assign(struct.get('assignees', ''))
        self.map.registers['public'].assign(struct.get('public', ''))
        self.map.registers['source'].assign(struct.get('source', ''))
        self.map.registers['destination'].assign(struct.get('destination', ''))
        self.map.registers['labels'].assign(struct.get('labels', ''))
        self.map.registers['url'].assign(struct.get('url', ''))
        self.map.registers['start'].assign(struct.get('start', ''))
        self.map.registers['ack'].assign(struct.get('ack', ''))
        self.map.registers['stop'].assign(struct.get('stop', ''))
        self.map.registers['deadline'].assign(struct.get('deadline', ''))
        self.map.registers['duration'].assign(struct.get('duration', ''))
        self.map.registers['comments'].assign(struct.get('comments', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['checked'].assign(struct.get('checked', ''))      
        self.map.registers['checked_by'].assign(struct.get('checked_by', ''))
        self.map.registers['updated_by'].assign(struct.get('updated_by', ''))
        self.map.registers['created_by'].assign(struct.get('created_by', ''))
        self.map.registers['updated_at'].assign(struct.get('updated_at', ''))
        self.map.registers['created_at'].assign(struct.get('created_at', ''))
        self.map.registers['last_modified'].assign(struct.get('last_modified', ''))
        # end of the map stuff
        self.map.store()


        "uuid": event.registers['uuid'].value,
        "account": event.registers['title'].value,
        "title": event.registers['title'].value,
        "description": event.registers['description'].value,
        "payload": event.registers['payload'].value,
        "assignees": event.registers['assignees'].value,
        "public",
        "source",
        "destination",
        "labels",
        "url",
        "start",
        "ack",
        "stop",
        "deadline",
        "duration",
        "comments",
        "status",
        "checked",
        "checked_by",
        "updated_by",
        "created_by",
        "updated_at",
        "created_at",
        "last_modified"

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
            "hello_message":event.registers['hello_message'].value,
            "saludation":event.registers['saludation'].value,
            "labels":event.registers['labels'].value,
            "number_type":event.registers['number_type'].value,
            "first_name":event.registers['first_name'].value,
            "last_name":event.registers['last_name'].value,
            "vendor_name":event.registers['vendor_name'].value,
            "reports_to":event.registers['reports_to'].value,
            "skype_id":event.registers['skype_id'].value,
            "mobile":event.registers['mobile'].value,
            "home_phone":event.registers['home_phone'].value,
            "other_phone":event.registers['other_phone'].value,
            "fax":event.registers['fax'].value,
            "campaign_source":event.registers['campaign_source'].value,
            "lead_source":event.registers['lead_source'].value,
            "title":event.registers['title'].value,
            "department":event.registers['department'].value,
            "phone_number":event.registers['phone_number'].value,
            "phone":event.registers['phone'].value,
            "cel_phone":event.registers['cel_phone'].value,
            "phone_numbers":event.registers['phone_numbers'].value,
            "country":event.registers['country'].value,
            "location":event.registers['location'].value,
            "timezone":event.registers['timezone'].value,
            "comments":event.registers['comments'].value,
            "status":event.registers['status'].value,
            "city":event.registers['city'].value,
            "state":event.registers['state'].value,
            "zip_code":event.registers['zip_code'].value,
            "date_of_birth":event.registers['date_of_birth'].value,
            "checked":event.registers['checked'].value,
            "do_not_disturb":event.registers['do_not_disturb'].value,
            "secondary_email":event.registers['secondary_email'].value,
            "assistant":event.registers['assistant'].value,
            "asst_phone":event.registers['asst_phone'].value,
            "address":event.registers['address'].value,
            "email":event.registers['email'].value,
            "email_opt_out":event.registers['email_opt_out'].value,
            "phone_opt_out":event.registers['phone_opt_out'].value,
            "deleted":event.registers['deleted'].value,
            "disabled":event.registers['disabled'].value,
            "description":event.registers['description'].value,
            "created_by":event.registers['created_by'].value,
            "modified_by":event.registers['modified_by'].value,            
        }
        return json.dumps(struct)

    def to_dict(self):
        event = self.map.reload()
        struct = {
            "uuid":event.registers['uuid'].value,
            "account":event.registers['account'].value,
            "hello_message":event.registers['hello_message'].value,
            "saludation":event.registers['saludation'].value,
            "labels":event.registers['labels'].value,
            "number_type":event.registers['number_type'].value,
            "first_name":event.registers['first_name'].value,
            "last_name":event.registers['last_name'].value,
            "vendor_name":event.registers['vendor_name'].value,
            "reports_to":event.registers['reports_to'].value,
            "skype_id":event.registers['skype_id'].value,
            "mobile":event.registers['mobile'].value,
            "home_phone":event.registers['home_phone'].value,
            "other_phone":event.registers['other_phone'].value,
            "fax":event.registers['fax'].value,
            "campaign_source":event.registers['campaign_source'].value,
            "lead_source":event.registers['lead_source'].value,
            "title":event.registers['title'].value,
            "department":event.registers['department'].value,
            "phone_number":event.registers['phone_number'].value,
            "phone":event.registers['phone'].value,
            "cel_phone":event.registers['cel_phone'].value,
            "phone_numbers":event.registers['phone_numbers'].value,
            "country":event.registers['country'].value,
            "location":event.registers['location'].value,
            "timezone":event.registers['timezone'].value,
            "comments":event.registers['comments'].value,
            "status":event.registers['status'].value,
            "city":event.registers['city'].value,
            "state":event.registers['state'].value,
            "zip_code":event.registers['zip_code'].value,
            "date_of_birth":event.registers['date_of_birth'].value,
            "checked":event.registers['checked'].value,
            "do_not_disturb":event.registers['do_not_disturb'].value,
            "secondary_email":event.registers['secondary_email'].value,
            "assistant":event.registers['assistant'].value,
            "asst_phone":event.registers['asst_phone'].value,
            "address":event.registers['address'].value,
            "email":event.registers['email'].value,
            "email_opt_out":event.registers['email_opt_out'].value,
            "phone_opt_out":event.registers['phone_opt_out'].value,
            "deleted":event.registers['deleted'].value,
            "disabled":event.registers['disabled'].value,
            "description":event.registers['description'].value,
            "created_by":event.registers['created_by'].value,
            "modified_by":event.registers['modified_by'].value,            
        }
        return struct