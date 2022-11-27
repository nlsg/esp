#!/usr/bin/env python3

"""micro_func provides some simple, pure functions, to make life easier"""

tee = lambda f, a: (a, f(a))[0]

def Debug(name="", surround=("[", "] "), debug=True, func=print, io=None):
    """returns a debugger function - which is print by default -
    if debug is true, else it returns a void function"""
    if not debug:
        func = lambda *_: None
    return lambda *m: func(surround[0] + name + surround[1], *m)

def callif(obj):
    if hasattr(obj, "__call__"):
        return obj()
    return obj

def trying(exception, function, arg, on_fail=lambda _, _i, a: None):
    """tries to return function(arg),
    returns on_fail(arg) if exception occures"""
    try:
        return function(arg)
    except exception:
        return on_fail(exception, function, arg)

def remove_chars(string, chars):
    # returns string without chars
    for char in chars:
        string = string.replace(char, "")
    return string

# has checks for a key, but does not throw en error if the obj is not a dict
has = lambda o, k: isinstance(o, dict) and k in o
