#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
import SocketServer
import marshal
import types
import base64
import pickle
import socket 
import argparse


# threaded xmlrpc
#import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer): pass
class RemotelyException(Exception): pass


DEBUG_MODE = False

class RemotelyServer(AsyncXMLRPCServer):
    def __init__(self, *args, **kwds):
        SimpleXMLRPCServer.__init__(self, *args, **kwds)
        self.api_key = None

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SimpleXMLRPCServer.server_bind(self)

    def register_key(self, api_key):
        self.api_key = api_key

    def run(self, api_key, func_str, *args, **kwds):
        if api_key != self.api_key:
            raise RemotelyException(" Bad API KEY: " + api_key)
    
        code = marshal.loads(base64.b64decode(func_str))
        func = types.FunctionType(code, globals(), "remote_func")
        
        if DEBUG_MODE:
            print "exec function", func
            print "func params", args, kwds

        output = func(*args, **kwds)
        output = base64.b64encode(pickle.dumps(output))
        return output


def main():
    #cmd options 
    parser = argparse.ArgumentParser(description='Simple and secure remote code execution.')
    parser.add_argument('--port', dest='port', action='store', type=int, default=8075,
                   help='server port (default to 8075)')
    parser.add_argument('--api_key', dest='api_key', action='store', required=True,
                   help='api key for authenticating against this server.')
    parser.add_argument('--daemon', dest='daemon', action='store_true', default=False,
                   help='run server as daemon (default false).')

    args = parser.parse_args()
    #print "HOST", args.host, args.port
    #print "API_KEY", args.api_key
    
    # start server
    def start_server():
        #server = RemotelyServer(('', args.port), AuthRequestHandler)
        server = RemotelyServer(('', args.port))
        server.register_multicall_functions()
        server.register_function(server.run, "run")
        server.register_key(args.api_key)
        print "starting remote exec server on port %s .." % args.port
        server.serve_forever()

    if args.daemon:
        print "@TODO: daemon mode"
        #import daemon
        #with daemon.DaemonContext():
        #    start_server()
    else:
        start_server()


if __name__=="__main__":
    main()        

