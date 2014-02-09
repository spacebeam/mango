# -*- coding: utf-8 -*-
'''
    Mango system models and messages.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


'''
	Text models are incredibly powerful.

	Maxwell's equations describe classical electrodynamic in four textual equations.

	In some domains pictures are great - show me a photo of a rose, a plan of house, or a set of equations describing the
	motions of the planets. No one descriptive method is best.

	/Joe
'''

'''
	expand on unix pipelines, there is a cool old video on your youtube history.
'''



class SimpleResource(models.Model):
    '''
        Mango simple resource
    '''
    contains = compound.ListType(types.UUIDType())

    total = types.IntType()


class Resource(models.Model):
    ''' 
        Mango resource
    '''
    apps = compound.ModelType(SimpleResource)
    calls = compound.ModelType(SimpleResource)
    queues = compound.ModelType(SimpleResource)
    records = compound.ModelType(SimpleResource)

    total = types.IntType()
