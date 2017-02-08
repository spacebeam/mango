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
            Task structure from your mango.
        '''
        bucket = client.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
        bucket.set_properties({'search_index': search_index})
        self.map = Map(bucket, None)

        self.map.registers['uuid'].assign(struct.get('uuid', ''))
        self.map.registers['account'].assign(struct.get('account', ''))
        self.map.registers['hello_message'].assign(struct.get('hello_message', ''))
        self.map.registers['saludation'].assign(struct.get('saludation', ''))
        self.map.registers['labels'].assign(struct.get('labels', ''))
        self.map.registers['number_type'].assign(struct.get('number_type', ''))
        self.map.registers['first_name'].assign(struct.get('first_name', ''))
        self.map.registers['last_name'].assign(struct.get('last_name', ''))
        self.map.registers['vendor_name'].assign(struct.get('vendor_name', ''))
        self.map.registers['reports_to'].assign(struct.get('reports_to', ''))
        self.map.registers['skype_id'].assign(struct.get('skype_id', ''))
        self.map.registers['mobile'].assign(struct.get('mobile', ''))
        self.map.registers['home_phone'].assign(struct.get('home_phone', ''))
        self.map.registers['other_phone'].assign(struct.get('other_phone', ''))
        self.map.registers['fax'].assign(struct.get('fax', ''))
        self.map.registers['campaign_source'].assign(struct.get('campaign_source', ''))
        self.map.registers['lead_source'].assign(struct.get('lead_source', ''))
        self.map.registers['title'].assign(struct.get('title', ''))
        self.map.registers['department'].assign(struct.get('department', ''))
        self.map.registers['phone_number'].assign(struct.get('phone_number', ''))
        self.map.registers['phone'].assign(struct.get('phone', ''))
        self.map.registers['cel_phone'].assign(struct.get('cel_phone', ''))
        self.map.registers['phone_numbers'].assign(struct.get('phone_numbers', ''))
        self.map.registers['country'].assign(struct.get('country', ''))
        self.map.registers['location'].assign(struct.get('location', ''))
        self.map.registers['timezone'].assign(struct.get('timezone', ''))
        self.map.registers['comments'].assign(struct.get('comments', ''))
        self.map.registers['status'].assign(struct.get('status', ''))
        self.map.registers['city'].assign(struct.get('city', ''))
        self.map.registers['state'].assign(struct.get('state', ''))
        self.map.registers['zip_code'].assign(struct.get('zip_code', ''))
        self.map.registers['date_of_birth'].assign(struct.get('date_of_birth', ''))
        self.map.registers['checked'].assign(struct.get('checked', ''))
        self.map.registers['do_not_disturb'].assign(struct.get('do_not_disturb', ''))
        self.map.registers['secondary_email'].assign(struct.get('secondary_email', ''))
        self.map.registers['assistant'].assign(struct.get('assistant', ''))
        self.map.registers['asst_phone'].assign(struct.get('asst_phone', ''))
        self.map.registers['address'].assign(struct.get('address', ''))
        self.map.registers['email'].assign(struct.get('email', ''))
        self.map.registers['email_opt_out'].assign(struct.get('email_opt_out', ''))
        self.map.registers['phone_opt_out'].assign(struct.get('phone_opt_out', ''))
        self.map.registers['deleted'].assign(struct.get('deleted', ''))
        self.map.registers['disabled'].assign(struct.get('disabled', ''))
        self.map.registers['description'].assign(struct.get('description', ''))
        self.map.registers['created_by'].assign(struct.get('created_by', ''))
        self.map.registers['modified_by'].assign(struct.get('modified_by', ''))
        
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