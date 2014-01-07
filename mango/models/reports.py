# -*- coding: utf-8 -*-
'''
    Mango reports data models
'''
# This file is part of mango.
#
# Distributed under the terms of the last AGPL License. The full
# license is in the file LICENCE, distributed as part of this
# software.

__author__ = 'Jean Chassoul'


from schematics import models
from schematics import types
from schematics.types import compound

from mango.models import records


class BaseResult(models.Model):
    '''
        Mango base result
    '''
    results = compound.ListType(compound.ModelType(records.Record))