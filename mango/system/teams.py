# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Team Machine'


import arrow
import uuid
import logging
import ujson as json
from tornado import gen
from schematics.types import compound
from mango.system import update_struct, remove_struct
from mango.messages import teams
from mango.messages import BaseResult
from mango.structures.teams import TeamMap
from riak.datatypes import Map
from mango.tools import clean_response, clean_structure
from mango.tools import get_search_item, get_search_list
from tornado import httpclient as _http_client


_http_client.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
http_client = _http_client.AsyncHTTPClient()


class TeamsResult(BaseResult):
    '''
        List result
    '''
    results = compound.ListType(compound.ModelType(teams.Team))


class Teams(object):
    '''
        Teams
    '''
    @gen.coroutine
    def get_team(self, account, team_uuid):
        '''
            Get team
        '''
        search_index = 'mango_team_index'
        query = 'uuid_register:{0}'.format(team_uuid)
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        url = get_search_item(self.solr, search_index, query, filter_query)
        # init got response list
        got_response = []
        # init crash message
        message = {'message': 'not found'}
        # ignore riak fields
        __ignore = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
        # hopefully asynchronous handle function request
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                # don't be careless with the time.
                yield gen.sleep(0.0021)
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response = stuff['response']['docs'][0]
                message = clean_response(response, __ignore)
        except Exception as error:
            logging.warning(error)
        return message

    @gen.coroutine
    def get_team_list(self, account, start, end, lapse, status, page_num):
        '''
            Get team list
        '''
        search_index = 'mango_team_index'
        query = 'uuid_register:*'
        filter_status = 'status_register:active'
        filter_account = 'account_register:{0}'.format(account.decode('utf-8'))

        # page number
        page_num = int(page_num)
        page_size = self.settings['page_size']
        start_num = page_size * (page_num - 1)

        filter_query = '(({0})AND({1}))'.format(filter_status, filter_account)
        url = get_search_list(self.solr, search_index, query, filter_query, start_num, page_size)

        # init got response list
        got_response = []
        # clean response message
        message = {
            'count': 0,
            'page': page_num,
            'results': []
        }
        __ignore = ["_yz_id","_yz_rk","_yz_rt","_yz_rb"]
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                # don't be careless with the time.
                yield gen.sleep(0.0021)
            stuff = got_response[0]
            if stuff['response']['numFound']:
                message['count'] += stuff['response']['numFound']
                for doc in stuff['response']['docs']:
                    message['results'].append(clean_response(doc, __ignore))
            else:
                logging.error('there is probably something wrong! get list campaign')
        except Exception as error:
            logging.warning(error)
        return message
    
    @gen.coroutine
    def uuid_from_account(self, username):
        '''
            Get uuid from username account
        '''
        search_index = 'mango_account_index'
        query = 'account_register:{0}'.format(username)
        filter_query = 'account_register:{0}'.format(username)

        url = get_search_item(self.solr, search_index, query, filter_query)
        # init got response list
        got_response = []
        # init crash message
        message = {'message': 'not found'}
        # ignore riak fields
        __ignore = [
            "_yz_id","_yz_rk","_yz_rt","_yz_rb",
            # CUSTOM FIELDS
            "name_register",
            "description_register",
            "teams_register",
            "members_register"
        ]
        # hopefully asynchronous handle function request
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                # don't be careless with the time.
                yield gen.sleep(0.0021)
            stuff = got_response[0]
            if stuff['response']['numFound']:
                response = stuff['response']['docs'][0]
                message = clean_response(response, __ignore)
        except Exception as error:
            logging.warning(error)        
        return message['uuid']

    @gen.coroutine
    def add_team(self, username, org_account, org_uuid, team_name, team_uuid):
        '''
            add (ORG) team
        '''
        user_uuid = yield self.uuid_from_account(username)
        orgs_url = 'https://{0}/orgs/{1}'.format(self.domain, org_uuid)
        user_url = 'https://{0}/users/{1}'.format(self.domain, user_uuid)
        # got callback response?
        got_response = []
        # yours truly
        headers = {'content-type':'application/json'}
        # and know for something completly different
        orgs = {
            'account': org_account,
            'teams': [{'uuid':team_uuid,
                       'name':team_name}],
            'last_update_at': arrow.utcnow().timestamp,
            'last_update_by': username,
        }
        users = {
            'account': username,
            'teams': [{"uuid":team_uuid,
                       "name":team_name,
                       "org":org_account}],
            'last_update_at': arrow.utcnow().timestamp,
            'last_update_by': username,
        }
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                orgs_url,
                method='PATCH',
                headers=headers,
                body=json.dumps(orgs),
                callback=handle_request
            )
            http_client.fetch(
                user_url,
                method='PATCH',
                headers=headers,
                body=json.dumps(users),
                callback=handle_request
            )
            while len(got_response) <= 1:
                # don't be careless with the time.
                yield gen.sleep(0.0021)            
        except Exception as error:
            logging.error(error)
        return got_response[0]

    @gen.coroutine
    def new_team(self, struct):
        '''
            New team event
        '''
        search_index = 'mango_team_index'
        bucket_type = 'mango_team'
        bucket_name = 'teams'
        try:
            event = teams.Team(struct)
            event.validate()
            event = clean_structure(event)
        except Exception as error:
            raise error
        try:
            message = event.get('uuid')
            structure = {
                "uuid": str(event.get('uuid', str(uuid.uuid4()))),
                "account": str(event.get('account', 'pebkac')),
                "status": str(event.get('status', '')),
                "name": str(event.get('name', '')),
                "permission": str(event.get('permission', '')),
                "members": str(event.get('members', '')),
                "resources": str(event.get('resources', '')),
                "labels": str(event.get('labels', '')),
                "history": str(event.get('history', '')),
                "checked": str(event.get('checked', '')),
                "checked_by": str(event.get('checked_by', '')),
                "checked_at": str(event.get('checked_at', '')),
                "created_by": str(event.get('created_by', '')),
                "created_at": str(event.get('created_at', '')),
                "last_update_by": str(event.get('last_update_by', '')),
                "last_update_at": str(event.get('last_update_at', '')),
                "description": str(event.get('description', '')),
            }
            result = TeamMap(
                self.kvalue,
                bucket_name,
                bucket_type,
                search_index,
                structure
            )
            message = structure.get('uuid')
        except Exception as error:
            logging.error(error)
            message = str(error)
        return message

    @gen.coroutine
    def modify_team(self, account, team_uuid, struct):
        '''
            Modify team
        '''
        # riak search index
        search_index = 'mango_team_index'
        # riak bucket type
        bucket_type = 'mango_team'
        # riak bucket name
        bucket_name = 'teams'
        # solr query
        query = 'uuid_register:{0}'.format(team_uuid.rstrip('/'))
        # filter query
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # search query url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        logging.warning(url)
        
        # pretty please, ignore this list of fields from database.
        IGNORE_ME = ("_yz_id","_yz_rk","_yz_rt","_yz_rb","checked","keywords")
        # got http callback response
        got_response = []
        # default return message
        message = {'update_complete':False}
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                # don't be careless with the time.
                yield gen.sleep(0.0010)
            response = got_response[0].get('response')['docs'][0]
            riak_key = str(response['_yz_rk'])
            bucket = self.kvalue.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
            bucket.set_properties({'search_index': search_index})
            team = Map(bucket, riak_key)
            # TODO: measure if there is value on make update_struct a yielding coroutine!
            message['update_complete'] = update_struct(team, struct, IGNORE_ME)
        except Exception as error:
            logging.exception(error)
        return message.get('update_complete', False)

    @gen.coroutine
    def modify_remove(self, account, team_uuid, struct):
        '''
            Modify remove
        '''
        # riak search index
        search_index = 'mango_team_index'
        # riak bucket type
        bucket_type = 'mango_team'
        # riak bucket name
        bucket_name = 'teams'
        # solr query
        query = 'uuid_register:{0}'.format(team_uuid.rstrip('/'))
        # filter query
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        # search query url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        # pretty please, ignore this list of fields from database.
        IGNORE_ME = ("_yz_id","_yz_rk","_yz_rt","_yz_rb","checked","keywords")
        # got callback response?
        got_response = []
        # yours truly
        message = {'update_complete':False}
        def handle_request(response):
            '''
                Request Async Handler
            '''
            if response.error:
                logging.error(response.error)
                got_response.append({'error':True, 'message': response.error})
            else:
                got_response.append(json.loads(response.body))
        try:
            http_client.fetch(
                url,
                callback=handle_request
            )
            while len(got_response) == 0:
                # Please, don't be careless with the time.
                yield gen.sleep(0.0010)
            response = got_response[0].get('response')['docs'][0]
            riak_key = str(response['_yz_rk'])
            bucket = self.kvalue.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
            bucket.set_properties({'search_index': search_index})
            team = Map(bucket, riak_key)
            for key in struct:
                if key not in IGNORE_ME:
                    if type(struct.get(key)) == list:
                        team.reload()
                        old_value = team.registers['{0}'.format(key)].value
                        if old_value:
                            old_list = json.loads(old_value.replace("'",'"'))
                            new_list = [x for x in old_list if x not in struct.get(key)]
                            team.registers['{0}'.format(key)].assign(str(new_list))
                            team.update()
                            message['update_complete'] = True
                    else:
                        message['update_complete'] = False
        except Exception as error:
            logging.exception(error)
        return message.get('update_complete', False)

    @gen.coroutine
    def remove_team(self, account, team_uuid):
        '''
            Remove team
        '''
        # Yo, missing history ?
        struct = {}
        struct['status'] = 'deleted'
        message = yield self.modify_team(account, team_uuid, struct)
        return message
