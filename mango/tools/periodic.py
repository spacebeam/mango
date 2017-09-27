# -*- coding: utf-8 -*-
'''
    Mango tools system periodic functions.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Team Machine'

import logging
from tornado import httpclient
import ujson as json
import uuid
import urllib
from tornado import gen


httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')


# -- some of it is wrong buy we don't know what parts (=