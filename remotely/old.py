import xmlrpclib
import SocketServer
import marshal
import types
import base64
import pickle

# threaded xmlrpc
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass

class RemoteException(Exception):
    pass 

class RemoteServer():
    def __init__(self, host, port):
        url = "http://%s:%s" % (host, port)
        self.proxy = xmlrpclib.ServerProxy(url, allow_none=True)

    def require(self, module_name):
        pass

    def run(self, func, *args, **kwds):
        code_str = base64.b64encode(marshal.dumps(func.func_code))
        output = self.proxy.run(code_str, *args, **kwds)
        return pickle.loads(base64.b64decode(output))

    @classmethod
    def server_run(cls, func_str, *args, **kwds):
        print "func size", len(func_str)
        print "func args", args
        print "func kwds", kwds
        code = marshal.loads(base64.b64decode(func_str))
        func = types.FunctionType(code, globals(), "remote_func")
        print "executing function", func
        output = func(*args, **kwds)
        output = base64.b64encode(pickle.dumps(output))
        return output


def main():
    server = AsyncXMLRPCServer(('', 9000), SimpleXMLRPCRequestHandler) 
    server.register_multicall_functions()
    server.register_function(ExecServer.server_run, "run")
    print "starting remote exec server on port 9000.."
    server.serve_forever()
    
    

if __name__=="__main__":
    main()        
