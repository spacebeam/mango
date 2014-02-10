# -*- coding: utf-8 -*-
'''
	Mango billings models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


from schematics import models
from schematics import types


class Route(models.Model):
    '''
    	Mango route

        Route billing model used for calculate the call cost
    '''
    dst = types.StringType(required=False)
    channel = types.StringType(required=True)
    dchannel = types.StringType(required=True)
    cost = types.IntType(required=True)