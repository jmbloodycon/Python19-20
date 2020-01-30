import unittest
import socket
import operations as m
import Server
from Storage import Storage


class KVStorageTests(unittest.TestCase):
    HOST = '127.0.0.1'
    PORT = 2010

    def test_init(self):
        storage = Storage()
        conn = self.PORT
        server = Server.ServerThread(conn, storage)
        self.assertEquals(server.conn, conn)
