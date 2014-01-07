#!/usr/bin/env python
'''
    Mango data indexes
'''


def ensure_indexes(db):
    '''
        Mango ensure indexes
        
        Ensure indexes function
        
        This function create the indexes on the MongoDB BSON database,
        more about mongodb or BSON objects on the follow urls:
        
        (BSON)
        (MongoDB)
        
        ensure_indexes(db)
        
        Example: TBD on ipython notebook
        
    '''
    db.queues.ensure_index([('name', 1)], unique=True)
    db.accounts.ensure_index([('account', 1)], unique=True)
    db.accounts.ensure_index([('email', 1)], unique=True)
    
    #https://jira.mongodb.org/browse/SERVER-1068
    #db.accounts.ensure_index([('routes.dst', 1),
    #                          ('routes.channel',1), 
    #                          ('routes.dchannel',1)], unique=True)