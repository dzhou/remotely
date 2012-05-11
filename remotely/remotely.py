import xmlrpclib
import SocketServer
import marshal
import types
import base64
import pickle
import socket 


def remotely(api_key, host, port):
    """
    remotely decorator
    """
    def decorate(func):
        url = "http://%s@%s:%s" % (api_key, host, port)
        proxy = xmlrpclib.ServerProxy(url, allow_none=True)

        def wrapper(*args, **kwds):
            code_str = base64.b64encode(marshal.dumps(func.func_code))
            output = proxy.run(code_str, *args, **kwds)
            return pickle.loads(base64.b64decode(output))

        return wrapper
    return decorate

