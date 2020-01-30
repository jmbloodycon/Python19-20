import socket


class Client:
    HOST = '127.0.0.1'
    PORT = 2019

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.HOST, self.PORT))

        while True:
            try:
                raw_data = input('>> ')
                if raw_data == 'exit':
                    break
                if raw_data == 'stop':
                    sock.send(raw_data.encode())
                    break
                sock.send(raw_data.encode())
                result = sock.recv(1024)
                print(result.decode())
            except KeyboardInterrupt:
                break
        sock.close()


if __name__ == '__main__':
    client = Client()
    client.run()
