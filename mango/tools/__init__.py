# This file is part of mango.

# Distributed under the terms of the last AGPL License.


__author__ = 'Jean Chassoul'


import arrow
import ujson as json
import logging
import uuid
from tornado import gen


def validate_uuid4(uuid_string):
    '''
        Validate that a UUID string is in fact a valid uuid4.

        Happily, the uuid module does the actual checking.
    '''
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string
        # is not a valid hex code for a UUID.
        return False
    return str(val) == uuid_string


def get_average(total, marks):
    '''
        Get average from signals
    '''
    return float(total) / len(marks)


def get_percentage(part, whole):
    '''
        Get percentage of part and whole.

    '''
    return "{0:.0f}%".format(float(part)/whole * 100)


@gen.coroutine
def check_json(struct):
    '''
        Check for malformed JSON
    '''
    try:
        message = json.loads(struct)
    except Exception as error:
        message = json.dumps({'error': 400})
        raise error
    return message


@gen.coroutine
def check_times(start, end):
    '''
        Check times
    '''
    try:
        start = (arrow.get(start) if start
                 else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))
        message = {'start': start.timestamp, 'end': end.timestamp}
    except Exception as error:
        logging.exception(error)
        raise error
    return message


@gen.coroutine
def check_times_get_timestamp(start, end):
    '''
        Check times get timestamp
    '''
    try:
        start = (arrow.get(start) if start
                 else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))
        message = {'start': start.timestamp, 'end': end.timestamp}
    except Exception as error:
        logging.exception(error)
        raise error
    return message


@gen.coroutine
def check_times_get_datetime(start, end):
    '''
        Check times get datetime
    '''
    try:
        start = (arrow.get(start) if start
                 else arrow.get(arrow.utcnow().date()))
        end = (arrow.get(end) if end else start.replace(days=+1))
        message = {'start': start.naive, 'end': end.naive}
    except Exception as error:
        logging.exception(error)
        raise error
    return message


def clean_message(struct):
    '''
        clean message
    '''
    struct = struct.to_native()
    struct = {
        key: struct[key] for key in struct
        if struct[key] is not None
    }
    return struct


def clean_structure(struct):
    '''
        clean structure
    '''
    struct = struct.to_primitive()
    struct = {
        key: struct[key] for key in struct
        if struct[key] is not None
    }
    return struct


def clean_results(results):
    '''
        clean results
    '''
    results = results.to_primitive()
    results = results.get('results')
    results = [
        {
            key: dic[key] for key in dic
            if dic[key] is not None
        } for dic in results
    ]
    return {'results': results}


def str2bool(boo):
    '''
        String to boolean
    '''
    return boo.lower() in ('yes', 'true', 't', '1')
