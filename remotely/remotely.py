#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
import marshal
import base64
import pickle


def remotely(api_key, host, port):
    """
    decorator for executing code remotely
    @param api_key: key for authentication
    @param host: remotely server ip
    @param port: remotely server port
    """
    def decorate(func):
        url = "http://%s:%s" % (host, port)
        proxy = xmlrpclib.ServerProxy(url, allow_none=True)

        def wrapper(*args, **kwds):
            code_str = base64.b64encode(marshal.dumps(func.func_code))
            output = proxy.run(api_key, code_str, *args, **kwds)
            return pickle.loads(base64.b64decode(output))

        return wrapper
    return decorate

