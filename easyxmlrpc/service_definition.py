# -*- coding: utf-8 -*-

import inspect


class ServiceDefinition(object):
    """
    Class responsible to build a hierarchy between service name and
    functions names. Example,
        class FooService(object):

            @xmlrpc_method()
            def bar():
                ...

        ServiceDefinition('foo', FooService)
    it will build a XML-RPC method with 'foo.bar' as name.
    """
    def __init__(self, name, cls):
        self.name = name
        self.functions = self._get_xmlrpc_functions(cls)

    def _get_xmlrpc_functions(self, cls):
        functions = []
        for func in inspect.getmembers(cls, predicate=inspect.isfunction):
            function = func[1]
            if hasattr(function, 'name'):
                functions.append(function)
        return functions

    def get_function_name(self, function):
        if self.name:
            return '{}.{}'.format(self.name, function.name)
        else:
            return function.name
