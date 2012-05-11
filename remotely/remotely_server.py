#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib
import SocketServer
import marshal
import types
import base64
import pickle
import socket 

# user optparse to support <= 2.6
#import argparse
from optparse import OptionParser


# threaded xmlrpc
#import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCServer,SimpleXMLRPCRequestHandler
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer): pass
class RemotelyException(Exception): pass


DEBUG_MODE = False

def create_remotely_server(api_key, port=8075):
    server = RemotelyServer(('', port))
    server.register_multicall_functions()
    server.register_function(server.run, "run")
    server.register_key(api_key)
    return server


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
        if api_key != self.api_key and self.api_key is not None:
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
    #parser = argparse.ArgumentParser(description='Simple and secure remote code execution.')
    #parser.add_argument('--port', dest='port', action='store', type=int, default=8075,
    #               help='server port (default to 8075)')
    #parser.add_argument('--api_key', dest='api_key', action='store', required=True,
    #               help='api key for authenticating against this server.')
    #parser.add_argument('--daemon', dest='daemon', action='store_true', default=False,
    #               help='run server as daemon (default false).')

    parser = OptionParser()
    parser.add_option("--port", dest="port", default=8075, type="int",
                    help="server port (default to 8075).")
    parser.add_option("--api_key", dest="api_key", default=None, type="string",
                    help="api key for authenticating against this server.")
    parser.add_option('--daemon', dest="daemon", action='store_true', default=False,
                    help='run server as daemon (default false).')

    (args, _) = parser.parse_args()

    if args.api_key is None:
        print "warning: starting server without API_KEY, anyone can access the server"
    
    # argparse code
    #args = parser.parse_args()
    #print "HOST", args.host, args.port
    #print "API_KEY", args.api_key
    
    def start_server():
        server = create_remotely_server(args.api_key, args.port)
        print "starting remote exec server on port %s .." % args.port
        server.serve_forever()

    if args.daemon:
        print "warning: daemon mode not available"
        #import daemon
        #with daemon.DaemonContext():
        #    start_server()
    else:
        start_server()
    return 0


if __name__=="__main__":
    main()        

