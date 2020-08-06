# This file is part of mango.

# Distributed under the terms of the last AGPL License.


__author__ = 'Jean Chassoul'


import riak
import logging
from tornado import gen
from schematics.types import compound
from mango.schemas import accounts
from mango.schemas import BaseResult
from mango.tools import clean_structure
from tornado import httpclient as _http_client

curl_client = 'tornado.curl_httpclient.CurlAsyncHTTPClient'
_http_client.AsyncHTTPClient.configure(curl_client)
http_client = _http_client.AsyncHTTPClient()


class UserResult(BaseResult):
    '''
        List result
    '''
    results = compound.ListType(compound.ModelType(accounts.Users))


class Accounts(object):
    '''
        Very self explanatory 
    '''

    @gen.coroutine
    def new_user(self, struct):
        '''
            New user event
        '''
        bucket_name = 'accounts'
        bucket = self.db.bucket(bucket_name)
        try:
            struct['created_by'] = self.settings['domain']
            event = accounts.Users(struct)
            event.validate()
            event = clean_structure(event)
        except Exception as error:
            raise error
        try:
            message = event.get('uuid')
            user = bucket.new(message, data=event)
            user.add_index("uuid_bin", message)
            user.add_index("status_bin", event["status"])
            user.add_index("account_bin", event["account"])
            user.add_index("account_type_bin", event["account_type"])
            user.add_index("email_bin", event["email"])
            user.store()
        except Exception as error:
            logging.error(error)
            message = str(error)
        return message

    @gen.coroutine
    def get_user(self, account, user_uuid):
        '''
            Get user
        '''
        bucket_name = 'accounts'
        bucket = self.db.bucket(bucket_name)
        results = bucket.get_index("uuid_bin", user_uuid)
        message = [y.data for y in (bucket.get(x) for x in results)]
        if message:
            message = message[0]
        else:
            message = {'message': 'not found'}
        return message

    @gen.coroutine
    def uuid_from_account(self, username):
        '''
            Get uuid from username account
        '''
        bucket_name = 'accounts'
        bucket = self.db.bucket(bucket_name)
        results = bucket.get_index("account_bin", username)
        message = [y.data for y in (bucket.get(x) for x in results)]
        if message:
            message = message[0]
        else:
            message = {'message': 'not found'}
        return message['uuid']

    @gen.coroutine
    def get_user_list(self, account, start, end, lapse, status, page_num):
        '''
            Get user account list
        '''

        # search_index = 'mango_account_index'
        # query = 'uuid_register:*'
        # filter_status = 'status_register:active'
        # filter_account_type = 'account_type_register:user'
        # page_num = int(page_num)
        # page_size = self.settings['page_size']
        # start_num = page_size * (page_num - 1)
        # filter_account = 'created_by_register:{0}'.format(account.decode('utf-8'))
        # filter_query = '(({0})AND({1})AND({2}))'.format(filter_account, filter_status, filter_account_type)
        # TODO: cool but WTF with account, start, end, lapse and status?

        result = []
        message = {
            'count': 0,
            'page': page_num,
            'results': result}
        upper_limit = 480000 * 3
        logging.info("upper_limit not being used! {} why?".format(upper_limit))
        page_num = int(page_num)
        page_size = self.settings['page_size']
        start_num = page_size * (page_num - 1)
        end_num = start_num + page_size
        bucket_name = 'accounts'
        bucket = self.db.bucket(bucket_name)
        query = bucket.stream_index("account_type_bin", 'user')
        for x in query:
            for y in x:
                result.append(y)
        message['count'] = len(result)
        message['results'] = [
            y.data for y in (bucket.get(x) for x in result[start_num:end_num])]
        return message

    @gen.coroutine
    def modify_account(self, account, user_uuid, struct):
        '''
            Modify account
        '''
        # riak search index
        search_index = 'mango_account_index'
        # riak bucket type
        bucket_type = 'mango_account'
        # riak bucket name
        bucket_name = 'accounts'
        # solr query
        query = 'uuid_register:{0}'.format(user_uuid.rstrip('/'))
        # filter query
        try:
            filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
            logging.warning(filter_query)
        except AttributeError:
            filter_query = 'account_register:{0}'.format(account)
            logging.warning(filter_query)
        # search query url
        url = "https://{0}/search/query/{1}?wt=json&q={2}&fq={3}".format(
            self.solr, search_index, query, filter_query
        )
        logging.warning(url)
        # pretty please, ignore this list of fields from database.
        IGNORE_ME = ("_yz_id","_yz_rk","_yz_rt","_yz_rb","checked","keywords")
        # got callback response?
        got_response = []
        # your message truly
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
                yield gen.sleep(0.0021)
            response = got_response[0].get('response')['docs'][0]
            riak_key = str(response['_yz_rk'])
            bucket = self.kvalue.bucket_type(bucket_type).bucket('{0}'.format(bucket_name))
            bucket.set_properties({'search_index': search_index})
            user = Map(bucket, riak_key)
            for key in struct:
                if key not in IGNORE_ME:
                    if type(struct.get(key)) == list:
                        user.reload()
                        old_value = user.registers['{0}'.format(key)].value
                        if old_value:
                            old_list = json.loads(old_value.replace("'",'"'))
                            for thing in struct.get(key):
                                old_list.append(thing)
                            user.registers['{0}'.format(key)].assign(str(old_list))
                        else:
                            new_list = []
                            for thing in struct.get(key):
                                new_list.append(thing)
                            user.registers['{0}'.format(key)].assign(str(new_list))
                    else:
                        user.registers['{0}'.format(key)].assign(str(struct.get(key)))
                    user.update()
            update_complete = True
            message['update_complete'] = True
        except Exception as error:
            logging.exception(error)
        return message.get('update_complete', False)

    @gen.coroutine
    def remove_account(self, account, user_uuid):
        '''
            Remove account
        '''
        # Yo, missing history ?
        struct = {}
        struct['status'] = 'deleted'
        message = yield self.modify_account(account, user_uuid, struct)
        return message
    
    @gen.coroutine
    def new_org(self, struct):
        '''
            New (ORG) event
        '''
        search_index = 'mango_account_index'
        bucket_type = 'mango_account'
        bucket_name = 'accounts'
        try:
            event = accounts.Org(struct)
            event.validate()
            event = clean_structure(event)
        except Exception as error:
            raise error
        try:
            message = event.get('uuid')
            structure = {
                "uuid": str(event.get('uuid', str(uuid.uuid4()))),
                "status": str(event.get('status', '')),
                "account": str(event.get('account', 'pebkac')),
                "account_type": str(event.get('account_type', 'org')),
                "name": str(event.get('name', '')),
                "description": str(event.get('description', '')),
                "email": str(event.get('email', '')),
                "phone_number": str(event.get('phone_number', '')),
                "extension": str(event.get('extension', '')),
                "country_code": str(event.get('country_code', '')),
                "timezone": str(event.get('timezone', '')),
                "company": str(event.get('company', '')),
                "location": str(event.get('location', '')),
                "phones": str(event.get('phones', '')),
                "emails": str(event.get('emails', '')),
                "history": str(event.get('history', '')),
                "labels": str(event.get('labels', '')),
                "members": str(event.get('members', '')),
                "teams": str(event.get('teams', '')),
                "checked": str(event.get('checked', '')),
                "checked_by": str(event.get('checked_by', '')),
                "checked_at": str(event.get('checked_at', '')),
                "created_by": str(event.get('created_by', '')),
                "created_at": str(event.get('created_at', '')),
                "last_update_at": str(event.get('last_update_at', '')),
                "last_update_by": str(event.get('last_update_by', '')),
            }
            result = AccountMap(
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
    def add_org(self, username, org_account, org_uuid):
        '''
            Update user profile with (ORG)
        '''
        user_uuid = yield self.uuid_from_account(username)
        # Please, don't hardcode your shitty domain in here.
        url = 'https://{0}/users/{1}'.format(self.domain, user_uuid)
        logging.warning(url)
        # got callback response?
        got_response = []
        # yours trully
        headers = {'content-type':'application/json'}
        # and know for something completly different
        message = {
            'account': username,
            'orgs': [{"uuid":org_uuid,"account":org_account}],
            'last_update_at': arrow.utcnow().timestamp,
            'last_update_by': username,
        }
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
                method='PATCH',
                headers=headers,
                body=json.dumps(message),
                callback=handle_request
            )
            while len(got_response) == 0:
                # don't be careless with the time.
                yield gen.sleep(0.0021)
            #logging.warning(got_response)
        except Exception as error:
            logging.error(error)
            message = str(error)
        return message

    @gen.coroutine
    def get_org(self, account, org_uuid):
        '''
            Get (ORG)
        '''
        search_index = 'mango_account_index'
        query = 'uuid_register:{0}'.format(org_uuid)
        filter_query = 'account_register:{0}'.format(account.decode('utf-8'))
        url = get_search_item(self.solr, search_index, query, filter_query)
        logging.warning(url)
        # init got response list
        got_response = []
        # init crash message
        message = {'message': 'not found'}
        # ignore riak fields
        __ignore = [
            "_yz_id","_yz_rk","_yz_rt","_yz_rb",
            # CUSTOM FIELDS
            "nickname_register",
            "first_name_register",
            "last_name_register",
            "middle_name_register",
            "password_register",
            "orgs_register"
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
        return message

    @gen.coroutine
    def get_org_list(self, account, start, end, lapse, status, page_num):
        '''
            Get (ORG) list
        '''
        search_index = 'mango_account_index'
        query = 'uuid_register:*'
        filter_status = 'status_register:active'
        filter_account_type = 'account_type_register:org'
        # page number
        page_num = int(page_num)
        page_size = self.settings['page_size']
        start_num = page_size * (page_num - 1)

        # yo, tony was here!
        if account is False:
            filter_query = filter_status
            filter_query = '(({0})AND({1}))'.format(filter_status, filter_account_type)
        elif account is not False:
            filter_account = 'created_by_register:{0}'.format(account.decode('utf-8'))
            filter_query = '(({0})AND({1})AND({2}))'.format(filter_account, filter_status, filter_account_type)

        url = get_search_list(self.solr, search_index, query, filter_query, start_num, page_size)
        # init got response list
        got_response = []
        # init crash message
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
                logging.error('there is probably something wrong! get list orgs')
        except Exception as error:
            logging.warning(error)
        return message

