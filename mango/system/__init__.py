# -*- coding: utf-8 -*-

# This file is part of mango.

# Distributed under the terms of the last AGPL License.
# The full license is in the file LICENCE, distributed as part of this software.


__author__ = 'Team Machine'


import ujson as json


def remove_struct(crdt, struct, IGNORE_ME):
    '''
        And Now for Something Completely Different
    '''
    message = {}
    for key in struct:
        if key not in IGNORE_ME:
            if type(struct.get(key)) == list:
                crdt.reload()
                ovalue = crdt.registers['{0}'.format(key)].value
                if ovalue:
                    olist = json.loads(ovalue.replace("'",'"'))
                    nlist = [x for x in olist if x not in struct.get(key)]
                    crdt.registers['{0}'.format(key)].assign(str(nlist))
                    crdt.update()
                    message['update_complete'] = True
            else:
                message['update_complete'] = False
    return message

def update_struct(crdt, struct, IGNORE_ME):
    '''
        So Long, and Thanks for All the Fish!
    '''
    # TODO: can we clean this a little bit more please?
    for key in struct:
        if key not in IGNORE_ME:
            if type(struct.get(key)) == list:
                crdt.reload()
                ovalue = crdt.registers['{0}'.format(key)].value
                if ovalue:
                    # TODO: da fuck is this json.loads?
                    olist = json.loads(ovalue.replace("'",'"'))
                    for thing in struct.get(key):
                        olist.append(thing)
                    crdt.registers['{0}'.format(key)].assign(str(olist))
                else:
                    wlist = []
                    for stuff in struct.get(key):
                        wlist.append(stuff)
                    crdt.registers['{0}'.format(key)].assign(str(wlist))
            else:
                crdt.registers['{0}'.format(key)].assign(str(struct.get(key)))
            crdt.update()
    # bool return after we finish our computations!
    return True
