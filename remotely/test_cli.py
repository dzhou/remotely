import xmlrpclib
import SocketServer
import marshal
import types
import base64
import pickle

# threaded xmlrpc
#from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
#class AsyncXMLRPCServer(SocketServer.ThreadingMixIn,SimpleXMLRPCServer): pass


from test_serv import remotely


@remotely("localhost", 9000, "asdf2")
def run_test():
    import os 
    import sys 
    return range(10)



def main():
    print run_test()

    #host = "localhost"
    #port = 9000
    #url = "http://dzhou:42@%s:%s" % (host, port)
    #proxy = xmlrpclib.ServerProxy(url, allow_none=True)
    #print proxy.run_test()

    

if __name__=="__main__":
    main()        
