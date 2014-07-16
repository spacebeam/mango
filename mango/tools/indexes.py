# -*- coding: utf-8 -*-
'''
    Mango database indexes.
'''

# This file is part of mango.

# Distributed under the terms of the last AGPL License. 
# The full license is in the file LICENCE, distributed as part of this software.

__author__ = 'Jean Chassoul'


def ensure_indexes(db):
    '''        
        Ensure indexes function
        
        This function create the indexes on the MongoDB BSON database,
        more about mongodb or BSON objects on the follow urls:
        
        (BSON)
        (MongoDB)

        ensure_indexes(db)
    '''
    # db.queues.ensure_index([('name', 1)], unique=True)
    db.accounts.ensure_index([('account', 1)], unique=True)
    db.accounts.ensure_index([('email', 1)], unique=True)
    
    #https://jira.mongodb.org/browse/SERVER-1068

    #db.accounts.ensure_index([('routes.dst', 1),
    #                          ('routes.channel',1), 
    #                          ('routes.dchannel',1)], unique=True)