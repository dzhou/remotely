import xmlrpclib
import SocketServer
import marshal
import types
import base64
import pickle
import socket 

# threaded xmlrpc
import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer): pass

api_keys = {}


def server_run(func_str, *args, **kwds):
    print "func size", len(func_str)
    print "func args", args
    print "func kwds", kwds
    code = marshal.loads(base64.b64decode(func_str))
    func = types.FunctionType(code, globals(), "remote_func")
    print "executing function", func
    output = func(*args, **kwds)
    output = base64.b64encode(pickle.dumps(output))
    return output


class AuthRequestHandler(SimpleXMLRPCRequestHandler, object):

    def do_POST(self):
        (enctype, encstr) =  self.headers.get('Authorization').split()
        api_key = base64.standard_b64decode(encstr)
        print "auth", api_key
        if api_key in api_keys:
            return super(AuthRequestHandler, self).do_POST()
        else:   
            raise Exception("not auth")


class Server(AsyncXMLRPCServer):
    def __init__(self, *args, **kwds):
        SimpleXMLRPCServer.__init__(self, *args, **kwds)

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SimpleXMLRPCServer.server_bind(self)

    def register_key(self, api_key):
        api_keys[api_key] = True


def main():
    #server = AsyncXMLRPCServer(('', 9000), AuthRequestHandler) 
    server = Server(('', 9000), AuthRequestHandler)
    server.register_multicall_functions()
    server.register_function(server_run, "run")
    server.register_key("asdf")
    print "starting remote exec server on port 9000.."
    server.serve_forever()


if __name__=="__main__":
    main()        
