#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper


def disable():
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    return


def decorator(deco):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''

    def wrapper(f):
        return update_wrapper(deco(f), f)

    update_wrapper(wrapper, deco)
    return wrapper


@decorator
def countcalls(f):
    '''Decorator that counts calls made to the function decorated.'''

    def wrapper(*args):
        wrapper.calls = getattr(wrapper, 'calls', 0) + 1
        return f(*args)

    return wrapper


@decorator
def memo(f):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''

    def wrapper(*args):
        if not hasattr(wrapper, 'cache'):
            wrapper.cache = {}
        if args in wrapper.cache:
            return wrapper.cache[args]
        else:
            update_wrapper(wrapper, f)
            wrapper.cache[args] = f(*args)
            return f(*args)

    return wrapper


@decorator
def n_ary(f):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''

    def wrapper(x, *args):
        return x if not args else f(x, wrapper(*args))

    return wrapper


def trace(s):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''

    def wrapper(f):
        def wrapped(*args):
            signature = '{0}({1})'.format(f.__name__, ', '.join(map(repr, args)))
            indent = trace.level * s
            print '{0} --> {1}'.format(indent, signature)
            trace.level += 1
            try:
                result = f(*args)
                indent = (trace.level - 1) * s
                print '{0} <-- {1} == {2}'.format(indent, signature, result)
            finally:
                trace.level -= 1
            return result

        trace.level = 0
        return wrapped

    return wrapper


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)


def main():
    print foo(4, 3)
    print foo(4, 3, 2)
    print foo(4, 3)
    print "foo was called", foo.calls, "times"

    print bar(4, 3)
    print bar(4, 3, 2)
    print bar(4, 3, 2, 1)
    print "bar was called", bar.calls, "times"

    print fib.__doc__
    fib(3)
    print fib.calls, 'calls made'


if __name__ == '__main__':
    main()
