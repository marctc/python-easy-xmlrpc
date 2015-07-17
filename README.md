# python-easy-xmlrpc
A pythonic XML-RPC microframework inspired in Django to build clean and well structured XML-RPC APIs.

### Motivation

First of all if you need make a web API you probably should use REST instead of XML-RPC. However if you still want to use XML-RPC take a look to this package.

Python has `xmlrpc` module in the standard library to work with [XML-RPC protocol](https://en.wikipedia.org/wiki/XML-RPC). However it has some caveats when working with nested procedure calls. Let's take the example from the [original documentation](https://docs.python.org/3/library/xmlrpc.server.html) to define a XMLRPC method called `currentTime.getCurrentTime()`:

    class ExampleService:
        class currentTime:
            @staticmethod
            def getCurrentTime():
                return datetime.datetime.now()    
    server.register_instance(ExampleService(), allow_dotted_names=True)
    
This way of define methods has some problems:
* Class names are not defined in `CamelCase` and function names are not defined with `snake_case` which means that your code won't fit the PEP8 standards.
* Unnecessary class nesting.
* Use of `allow_dotted_names` which is considered harmful by the own documentation:
>    Warning: Enabling the allow_dotted_names option allows intruders to access your module’s global variables and may allow intruders to execute arbitrary code on your machine. Only use this example only within a secure, closed network. 

### How to use

Create a `services.py` where you define XML-RPC methods:

    from easyxmlrpc.decorators import xmlrpc_function
    
    class StatusService(object):
    
        @xmlrpc_function()
        def ping():
            return 'pong'
    
    class CurrentTimeService(object):
    
        @xmlrpc_function(name='getCurrentTime')
        def get_current_time():
            return datetime.datetime.now()
`xmlrpc_function` is a decorator which transforms functions in static methods and provide a function name that will be used when server registers XML-RPC functions. If `name` is not specified, it takes the own function name.

Then create a list of `ServiceDefinition`:

    from easyxmlrpc.service_definition import ServiceDefinition
    from .services import StatusService, CurrentTimeService
    
    services = [
        ServiceDefinition('', StatusService),
        ServiceDefinition('currentTime', CurrentTimeService)
    ]
`ServiceDefinition` is a class used to define a nesting hierarchy between a service name and function names. In this example it will create  `currentTime.<method_name>` as a base for the defined methods in `CurrentTimeService`.

Finally you can invoke a XMLRPC server in this way:

    from easyxmlrpc.server import EasyXMLRPCServer
    server = EasyXMLRPCServer(('localhost', 8000), services=services)
    server.run()

And we can connect to XMLRPC server as usual:

    import xmlrpc.client
    
    server_proxy = xmlrpc.client.ServerProxy('http://localhost:8000')
    server_proxy.ping()  #  return 'pong'
    server_proxy.currentDate.getCurrentDate() # return current date
