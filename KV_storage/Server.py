import socket
import operations
from Storage import Storage
from threading import Thread
import sys


class ServerThread(Thread):
    def __init__(self, conn, storage):
        super().__init__()
        self.conn = conn
        self.storage = storage

    def run(self):
        while True:
            try:
                data = self.conn.recv(1024)
                dec_data = data.decode()
                if dec_data == 'stop\r\n':
                    operations.save_state(self.storage)
                    self.conn.shutdown(1)
                    self.conn.close()
                    exit()
            except ConnectionAbortedError:
                break
            if not data:
                break
            result = operations.execute_command(self.storage, data.decode())
            self.conn.send(result.encode())

        self.conn.shutdown(1)
        self.conn.close()


def listen(storage):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind(('127.0.0.1', 2019))
    connection.listen(10)
    while True:
        current_connection, address = connection.accept()
        server = ServerThread(current_connection, storage)
        server.start()


if __name__ == "__main__":
    i_storage = Storage()
    i_storage.load()
    try:
        listen(i_storage)
    except KeyboardInterrupt:
        sys.exit(0)
