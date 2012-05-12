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

sys.path.insert(0, os.path.abspath('..'))
from remotely import remotely
from remotely import create_remotely_server
from remotely import RemotelyException


cell_changer_code = new.code(
    1, 1, 2, 0,
    ''.join([
        chr(dis.opmap['LOAD_FAST']), '\x00\x00',
        chr(dis.opmap['DUP_TOP']),
        chr(dis.opmap['STORE_DEREF']), '\x00\x00',
        chr(dis.opmap['RETURN_VALUE'])
    ]), 
    (), (), ('newval',), '<nowhere>', 'cell_changer', 1, '', ('c',), ()
)

def change_cell_value(cell, newval):
    return new.function(cell_changer_code, {}, None, (), (cell,))(newval)

def test_mul(a, b):
    return a*b

def code_str(func):
    return base64.b64encode(marshal.dumps(func.func_code))

def decode_output(output):
    return pickle.loads(base64.b64decode(output))


class RemotelyServerTest(unittest.TestCase):

    def setUp(self):
        self.api_key = "test-api"
        self.port = random.randint(10000,60000)
        self.server = create_remotely_server(self.api_key, self.port)

    def tearDown(self):
        self.server.server_close()
        self.server = None

    def test_server(self):
        self.assertEqual(self.server.api_key, self.api_key)
        func = code_str(test_mul)

        # send req with bad key
        self.assertRaises(RemotelyException, self.server.run, None, func, 2, 3)
        self.assertRaises(RemotelyException, self.server.run, "BAD-KEY", func, 2, 3)

        # send req with good key
        self.assertEqual(decode_output(self.server.run(self.api_key, func, 0, 3)), 0)
        self.assertEqual(decode_output(self.server.run(self.api_key, func, 2, 3)), 6)


    def test_decorator(self):   
        dec = remotely(self.api_key, 'localhost', 9856)
        remote_func = dec(test_mul)
        # override proxy with local server in closure
        change_cell_value(remote_func.func_closure[0], self.server)
                
        self.assertEqual(remote_func(2,3), 6)
        self.assertEqual(remote_func(0,10), 0)
        self.assertRaises(TypeError, remote_func, None, None)


if __name__ == '__main__':
    unittest.main()
