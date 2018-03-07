# -*- coding: utf-8 -*-
'''
    Periodic callback functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'


import logging
import ujson as json
from tornado import httpclient
from tornado import gen

httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')


# TODO: lol, yo.. here is some code 2 refactor, cuz u know!
# simplify and test my bru.

# Yo, hello old friend, we meet again!


@gen.coroutine
def new_team(self, username, org_uuid, org_account, struct):
    '''
        POST new team
    '''
    logging.warning('here we post a new team')
    user_uuid = yield self.uuid_from_account(username)
    url = 'https://nonsense.ws/orgs/{0}/teams/'.format(org_uuid)
    got_response = []
    headers = {'content-type':'application/json'}
    struct['members'] = ['{0}:{1}'.format(username, user_uuid)]
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
            method='POST',
            headers=headers,
            body=json.dumps(struct),
            callback=handle_request
        )
        while len(got_response) == 0:
            # don't be careless with the time.
            yield gen.sleep(0.0010)
        message = got_response[0].get('uuid')
    except Exception as error:
        logging.error(error)
        message = str(error)
    return message

@gen.coroutine
def add_team(self, username, org_uuid, org_account, team_name, team_uuid):
    '''
        Update user profile with team
    '''
    user_uuid = yield self.uuid_from_account(username)
    # Please, don't hardcode your shitty domain in here.
    url = 'https://nonsense.ws/users/{0}'.format(user_uuid)
    # got callback response?
    got_response = []
    # yours trully
    headers = {'content-type':'application/json'}
    # and know for something completly different
    message = {
        'account': username,
        'teams': [{"uuid":team_uuid,
                   "name":team_name,
                   "org":org_uuid,
                   "account":org_account}],
        'last_update_at': arrow.utcnow().timestamp,
        'last_update_by': username,
    }
    logging.warning(message)
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
            yield gen.sleep(0.0010)
        #logging.warning(got_response)
    except Exception as error:
        logging.error(error)
        message = str(error)
    return message
