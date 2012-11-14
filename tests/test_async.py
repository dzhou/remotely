#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import new, dis
import json
import unittest
import base64
import marshal
import pickle
import random
import time 
import multiprocessing as mp

sys.path.insert(0, os.path.abspath('..'))
from remotely import create_remotely_server
from remotely import RemotelyException
from remotely import RemoteClient

# run a server locally for testing
def run_local_server(api_key, port):
    server = create_remotely_server(api_key, port)
    server.serve_forever()

# few test functions 
def foo(a,b,c): return a+b+c
def foo2(a,b,c): import time; time.sleep(2);return a+b+c


class RemotelyServerTest2(unittest.TestCase):

    def setUp(self):
        self.api_key = "test-api"
        self.host = 'localhost'
        self.port = random.randint(10000,60000)
        self.server = mp.Process(target=run_local_server, args=(self.api_key, self.port))
        self.server.start()
        time.sleep(0.1)
        self.client = RemoteClient(self.api_key, self.host, self.port)

    def tearDown(self):
        self.server.terminate()
        self.server.join()
        self.server = None
        self.client = None

    def test_blocking_run(self):
        # function blocks and returns value
        self.client.set_async(False)
        output = self.client.run(foo, 2, 3, 4)
        self.assertEquals(output, 2+3+4)

    def test_async_run(self):    
        # function does not block and returns pid for join()
        pid = self.client.run(foo, 1, 2, 3)
        output = self.client.join(pid)
        self.assertTrue(pid > 0)
        self.assertEqual(output, 6)

    def test_join_timeout(self):
        # non-blocking join returns no output
        pid = self.client.run(foo2, "A","B","C")
        output = self.client.join(pid, 0.01)
        output2 = self.client.join(pid, 0.01)
        output3 = self.client.join(pid)
        self.assertTrue(output is None)
        self.assertTrue(output2 is None)
        self.assertEquals(output3, "ABC")

    def test_async_kill(self):
        # killed process, no output returned
        pid = self.client.run(foo2, 1, 2, 3)
        ret = self.client.kill(pid)
        output = self.client.join(pid)
        self.assertTrue(ret)
        self.assertEquals(output, None)
        

if __name__ == '__main__':
    unittest.main()
