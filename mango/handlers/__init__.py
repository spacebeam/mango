# -*- coding: utf-8 -*-
'''
    Mango HTTP base handlers.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


# Remember Gabo Naum
# http://www.youtube.com/watch?v=2k-JGuhyqKE

'''

    Protocols are contracts that describe the rights and obligations of each party.

    State machine protocol engine?

    Learn state machines!
    Code generation
    router sockets

    ping, pong if we're not talking.

    Python and erlang <3

'''

'''
    
    Focus is a matter of deciding what things you're not going to do.

    When it's done.

    Good design uses symmetry, symmetry is one way to achive simplicity, but it's important enough to be mentioned on its own.

    Nature uses it a lot, which is a good sign.

    There are two kinds of symmetry, repetition and recursion.

    recursion means repetition in subelements, like the pattern of veins in a leaf.




    System primitives and basic building blocks 
    -------------------------------------------

    Recursively construction of computing stuff.

    Mango handlers for records of stuff giving reports and billing information if needed.


'''

'''
    System primitives
    -----------------

    accounts, records, reports, billings.

    Account primitives:
        - users
        - orgs(ORGs) are composed by teams of users with different goals and strategies for achivements.

    Resource primitives:
        - records
        - reports
        - billing (if needed)

'''

# accounts: {users or/and orgs}

# teams: {users members of orgs teams}

# resources: {records, reports, billing}

'''
    Follow eve the black chuchawa
    -----------------------------

    HTTP status code is primarily divided into five groups for better
    explanation of request and responses between client and server as named:

    Informational 1XX,
    Successful 2XX,
    Redirection 3XX,

    Client Error 4XX
        and
            Server Error 5XX.
'''

# Wake the fuck up.

'''
    Call misha the gentle beast
    ---------------------------

    The Session Initiation Protocol (SIP) is a signalling protocol used for
    controlling communication sessions such as Voice over IP telephone calls.

    SIP is based around request/response transactions, in a similar manner to
    the Hypertext Transfer Protocol (HTTP).

    Each transaction consists of a SIP request (which will be one of several
    request methods), and at least one response.

    SIP responses specify a three-digit integer response code, which is one
    of a number of defined codes that detail the status of the request.

    These codes are grouped according to their first digit as
    
    Provisional 1XX,
    Success 2XX,
    Redirection 3XX,
    Client error 4XX,
        
    Server error 5XX
        and
            Global failure 6XX.
    
       
    For example; "1xx" for provisional responses with a code of 100–199.

    The SIP response codes are an extension to the HTTP response codes,
    although not all HTTP response codes are valid in SIP.

'''

import motor

from tornado import gen
from tornado import web

from mango.system import basic_authentication

from mango.tools import check_account_authorization
from mango.tools import errors

# TODO: Change username to the more general account variable name.

'''
    HTTP request methods
    --------------------

    HTTP defines methods (sometimes referred to as fucking verbs)
    to indicate the desired action to be performed on the Universal Unique
    Identified (Resource) node, cluster, cohort, cloud.

    What this resource represents, whether pre-existing data or data that
    is generated dynamically, depends on the implementation of the server.

    Often, the resource corresponds to a file or the output of an executable
    residing on the server.

    The HTTP/1.0 specification:
        section 8 defined the GET, POST and HEAD methods

    HTTP/1.1 specification:
        section 9 added 5 new methods: OPTIONS, PUT, DELETE, TRACE and CONNECT.

    By being specified in these documents their semantics are well known
    and can be depended upon.

    Any client can use any method and the server can be configured to support
    any combination of methods.

    If a method is unknown to an intermediate it will be treated as an unsafe
    and non-idempotent method.

    There is no limit to the number of methods that can be defined and this allows
    for future methods to be specified without breaking existing infrastructure.

    RFC5789 specified the PATCH method.


    so... after all that stuff, we're coding on:

    [GET]
        Requests a representation of the specified resource.

        Requests using GET should only retrieve data and should have no other effect.

        (This is also true of some other HTTP methods.)

    [HEAD]
        Asks for the response identical to the one that would correspond to a GET request,
        but without the response body.

        This is useful for retrieving meta-information written in response headers,
        without having to transport the entire content.

    POST
        Requests that the server accept the entity enclosed in the request as a new subordinate
        of the web resource identified by the URI.

        The data POSTed might be, as examples, an annotation for existing resources;
        a message for a bulletin board, newsgroup, mailing list, or comment thread;
        a block of data that is the result of submitting a web form to a data-handling process;
        or an item to add to a database.

    PUT
        Requests that the enclosed entity be stored under the supplied URI.

        If the URI refers to an already existing resource, it is modified; if the URI does
        not point to an existing resource, then the server can create the resource with that URI.

    DELETE
        Deletes the specified resource.

    [OPTIONS]
        Returns the HTTP methods that the server supports for the specified URL.

        This can be used to check the functionality of a web server by requesting '*'
        instead of a specific resource.

    PATCH
        Is used to apply partial modifications to a resource.
'''

# 7, 11 nightmares at 3 am.

'''
    SIP request methods
    -------------------

    The Session Initiation Protocol (SIP) is a signalling protocol
    used for controlling communication sessions such as Voice over IP
    telephone calls.

    SIP is based around request/response transactions, in a similar manner
    to the Hypertext Transfer Protocol (HTTP).

    Each transaction consists of a SIP request (which will be one of several request methods),
    and at least one response.

    SIP requests are the codes used by Session Initiation Protocol
    for communication.

    To complement them there are SIP responses, which generally indicate
    whether this request succeeded or failed, and in the latter case, why it failed.

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

class BaseHandler(web.RequestHandler):
    '''
        Mango Base Handler
    '''

    @property
    def sql(self):
        '''
            SQL database
        '''
        return self.application.sql

    @property
    def document(self):
        '''
            Document database
        '''
        return self.application.document

    @property
    def kvalue(self):
        '''
            Key-value database
        '''
        return self.application.kvalue

    @property
    def graph(self):
        '''
            Graph database
        '''
        return self.application.graph

    def initialize(self, **kwargs):
        ''' 
            Initialize the Base Handler
        '''
        super(BaseHandler, self).initialize(**kwargs)

        self.etag = None

        # system database
        self.db = self.settings['db']

        # zeromq greatness stuff

        # self.cdr_stream = self.settings['cdr_stream']

        # Tornado CDR periodic callbacks
        # self.cdr_periodic = self.settings['cdr_periodic']

        # Pagination settings
        self.page_size = self.settings['page_size']

    def set_default_headers(self):
        '''
            Mango default headers
        '''
        self.set_header("Access-Control-Allow-Origin", "ph3nix.com")

    def get_current_user(self):
        '''
            Return the username from a secure cookie
        '''
        return self.get_secure_cookie('username')

    def get_current_account(self):
        '''
            Return the account from a secure cookie
        '''
        return self.get_secure_cookie('account')
    

class HomeHandler(BaseHandler):
    '''
        Mango HomeHandler Quote experiment
    '''
    
    @web.asynchronous
    def get(self):
        '''
            Get some quotes
        '''
        hackers = quotes.Quotes()
        self.write({'quote': hackers.get()})
        self.finish()


@basic_authentication
class LoginHandler(BaseHandler):
    '''
        BasicAuth login
    ''' 

    @web.asynchronous
    @gen.engine
    def get(self):
        # redirect this shit out?
        next_url = '/'
        args = self.get_arguments('next')
        if args:
            next_url = args[0]

        account = yield motor.Op(check_account_authorization,
                                 self.db,
                                 self.username, 
                                 self.password)

        if not account:
            # 401? 
            self.set_status(403)
            self.set_header('WWW-Authenticate', 'Basic realm=mango')
            self.finish()
        else:
            self.set_secure_cookie('username', self.username)
            self.username, self.password = (None, None)

            # redirect where and why?
            # self.redirect(next_url)

            self.set_status(200)
            self.finish()


class LogoutHandler(BaseHandler):
    '''
        BasicAuth logout
    '''

    @web.asynchronous
    def get(self):
        '''
            Clear secure cookie
        '''
        self.clear_cookie('username')

        self.set_status(200)
        self.finish()