# -*- coding: utf-8 -*-
'''
    Mango test classes, all tests should inherit from one of these.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


import unittest
import logging
from tornado.testing import AsyncTestCase
import tornado.web
import tornado.ioloop


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger(self.__class__.__name__)


class BaseAsyncTest(AsyncTestCase):

    def setUp(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super(BaseAsyncTest, self).setUp()

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()