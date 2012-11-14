#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
import marshal
import base64
import pickle
import multiprocessing



def remotely(api_key, host, port):
    """
    synchronous decorator for executing code remotely. 
    @param api_key: key for authentication
    @param host: remotely server ip
    @param port: remotely server port
    """
    def decorate(func):
        url = "http://%s:%s" % (host, port)
        proxy = xmlrpclib.ServerProxy(url, allow_none=True)

        def wrapper(*args, **kwds):
            code_str = base64.b64encode(marshal.dumps(func.func_code))
            output = proxy.run(api_key, False, code_str, *args, **kwds)
            return pickle.loads(base64.b64decode(output))

        return wrapper
    return decorate


class RemoteClient(object):

    def __init__(self, api_key, host, port, async=True):
        """
        class for asynchronous remote execution
        """
        url = "http://%s:%s" % (host, port)
        self.proxy = xmlrpclib.ServerProxy(url, allow_none=True)
        self.api_key = api_key
        self.host = host
        self.port = port
        self.async = True

    def set_async(self, async=True):
        self.async = async

    def run(self, func, *args, **kwds):
        """
        run function on remote server
        @return pid for async    
        """
        code_str = base64.b64encode(marshal.dumps(func.func_code))
        output = self.proxy.run(self.api_key, self.async, code_str, *args, **kwds)
        return pickle.loads(base64.b64decode(output))

    def join(self, pid, timeout=None):
        """
        Block the calling thread until the function terminate or timeout occurs.
        @param pid: process id from run()
        @param timeout: if timeout is none then there's no timeout
        """
        output = self.proxy.join(self.api_key, pid, timeout)
        return pickle.loads(base64.b64decode(output))

    def kill(self, pid):
        """
        Terminate the process using Process.terminate() call
        @param pid: process id from run()
        """
        output = self.proxy.kill(self.api_key, pid, timeout=None)
        return pickle.loads(base64.b64decode(output))


