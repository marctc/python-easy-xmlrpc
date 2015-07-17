# -*- coding: utf-8 -*-

from xmlrpc.server import SimpleXMLRPCServer


class EasyXMLRPCServer(SimpleXMLRPCServer):
    """
    XML-RPC server that also registers functions defined by a list of
    ServiceDefinition classes.
    """

    def __init__(self, *args, **kwargs):
        self.services = kwargs.pop('services', None)
        super(EasyXMLRPCServer, self).__init__(*args, **kwargs)

    def register_functions(self):
        for service in self.services:
            for function in service.functions:
                self.register_function(function, service.get_function_name(function))

    def run(self):
        self.register_introspection_functions()
        self.register_functions()
        self.serve_forever()
