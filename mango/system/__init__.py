# -*- coding: utf-8 -*-
'''
    Mango primitives system logic.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'



'''
    System logic
    ------------

    Logic takes care of itself; all we have to do is to look and see how it does it.

    - Ludwig Wittgenstein
'''

'''
    Mango HTTP Requests
    -------------------

    GET

    POST

    PUT

    PATCH

    DELETE

    HEAD

    OPTIONS
'''

'''
    Mango SIP Requests
    ------------------

    SIP requests are the codes used by Session Initiation Protocol for communication. 
    To complement them there are SIP responses, which generally indicate whether this 
    request succeeded or failed, and in the latter case, why it failed.

    INVITE
        Indicates a client is being invited to participate in a call session.

    ACK 
        Confirms that the client has received a final response to an INVITE request.

    BYE 
        Terminates a call and can be sent by either the caller or the callee.

    CANCEL
        Cancels any pending request.

    OPTIONS
        Queries the capabilities of servers.

    REGISTER
        Registers the address listed in the To header field with a SIP server.

    PRACK
        Provisional acknowledgement.

    SUBSCRIBE
        Subscribes for an Event of Notification from the Notifier.

    NOTIFY
        Notify the subscriber of a new Event.

    PUBLISH 
        Publishes an event to the Server.

    INFO
        Sends mid-session information that does not modify the session state.

    REFER
        Asks recipient to issue SIP request (call transfer.)

    MESSAGE
        Transports instant messages using SIP.

    UPDATE
        Modifies the state of a session without changing the state of the dialog.
'''

# Mango HTTP Requests

# [ Get ]

# GET /records/record/keys/key


# [ Store ]

# POST /records/record/keys
# PUT /records/record/keys/key


# [ Update ]

# PATCH /records/record/keys/key


# [ Delete ]

# DELETE /records/record/keys/key


# [ Describe ]

# HEAD/INFO?

'''
    Research Cryptography
    ---------------------
    
    SHA512

'''

'''
    Quantum objects
    ---------------

    Remarkably, there exists a realm of physics for which mathematical assertions
    of simple symmetries in real objects cease to be approximations.

    That is the domain of quantum physics, which for the most part is the physics
    of very small, very simple objects such as electrons, protons, light, and atoms.

    Unlike everyday objects, objects such as electrons have very limited numbers
    of configurations, called states, in which they can exist. 

    This means that when symmetry operations such as exchanging the positions
    of components are applied to them, the resulting new configurations often
    cannot be distinguished from the originals no matter how diligent an observer is. 

    Consequently, for sufficiently small and simple objects the generic mathematical 
    symmetry assertion F(x) = x ceases to be approximate, and instead becomes an 
    experimentally precise and accurate description of the situation in the real world.

'''

'''
    Basic building blocks
    ---------------------

    Recursively construction of computing stuff.

    Mango handlers for records of stuff giving reports and billing information if needed.

'''

'''
    System primitives
    -----------------

    accounts, resources {records, reports, billings}.

    Account primitives:
        - users (HUMAN) normal people like you and me.
        - orgs (ORGs) are composed by teams of users.

    Resource primitives:
        - records
        - reports
        - billing (if needed)

'''

import base64


def basic_authentication(handler_class):
    '''
        basic authentication
        --------------------

        HTTP Basic Authentication Decorator

        @basic_authentication
    '''

    def wrap_execute(handler_execute):
        '''
            Execute basic authentication

            Wrapper execute function
        '''

        def basic_auth(handler, kwargs):
            '''
                Basic AUTH implementation
            '''
            auth_header = handler.request.headers.get('Authorization')
            if auth_header is None or not auth_header.startswith('Basic '):
                handler.set_status(403)
                handler.set_header('WWW-Authenticate', 'Basic '\
                                   'realm=mango')
                handler._transforms = []
                handler.finish()
                return False

            auth_decoded = base64.decodestring(auth_header[6:])
            handler.username, handler.password = auth_decoded.split(':', 2)

            print('A user just enter the dungeon! /api/ @basic_authentication')
            print('username', handler.username, 'password', handler.password)

            return True

        def _execute(self, transforms, *args, **kwargs):
            '''
                Execute the wrapped function
            '''
            if not basic_auth(self, kwargs):
                return False
            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)

    return handler_class