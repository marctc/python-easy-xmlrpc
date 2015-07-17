# -*- coding: utf-8 -*-


def xmlrpc_function(name=None):
    def decorator(function):
        if name:
            function.name = name
        else:
            function.name = function.__name__
        return staticmethod(function)
    return decorator
