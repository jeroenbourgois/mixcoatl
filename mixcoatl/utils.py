"""Common helper utilities for use with mixcoatl"""
from multiprocessing import Process, Queue

def uncamel(str):
    """Return the snake case version of :attr:`str`

    >>> uncamel('deviceId')
    'device_id'
    >>> uncamel('dataCenterName')
    'data_center_name'
    """
    import re
    s = lambda str: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str).lower().strip('_')
    return s(str)

def uncamel_keys(d1):
    """Return :attr:`d1` with all keys converted to snake case

    >>> d = {'myThings':[{'thingId':1,'someThings':{'firstThing':'a_thing'}}]}
    >>> uncamel_keys(d)
    {'my_things': [{'thing_id': 1, 'some_things': {'first_thing': 'a_thing'}}]}
    """
    d2 = dict()
    if not isinstance(d1, dict):
        return d1
    for k,v in d1.iteritems():
        new_key = uncamel(k)
        if isinstance(v, dict):
            d2[new_key] = uncamel_keys(v)
        elif isinstance(v, list):
            d2[new_key] = [uncamel_keys(item) for item in v]
        else:
            d2[new_key] = v
    return d2

def camelize(str):
    """Return the camel case version of a :attr:`str`

    >>> camelize('this_is_a_thing')
    'thisIsAThing'
    """
    s = ''.join([t.title() for t in str.split('_')])
    return s[0].lower()+s[1:]

def camel_keys(d1):
    """Return :attr:`d1` with all keys converted to camel case

    >>> b = {'my_things': [{'thing_id': 1, 'some_things': {'first_thing': 'a_thing'}}]}
    >>> camel_keys(b)
    {'myThings': [{'thingId': 1, 'someThings': {'firstThing': 'a_thing'}}]}
    """
    d2 = dict()
    if not isinstance(d1, dict):
        return d1
    for k, v in d1.iteritems():
        new_key = camelize(k)
        if isinstance(v, dict):
            d2[new_key] = camel_keys(v)
        elif isinstance(v, list):
            d2[new_key] = [camel_keys(item) for item in v]
        else:
            d2[new_key] = v
    return d2

def convert(input):
    """Return :attr:`input` converted from :class:`unicode` to :class:`str`

    >>> convert(u'bob')
    'bob'
    >>> convert([u'foo', u'bar'])
    ['foo', 'bar']
    >>> convert({u'foo':u'bar'})
    {'foo': 'bar'}
    """
    if isinstance(input, dict):
        return dict((convert(key), convert(value)) for key, value in input.iteritems())
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input