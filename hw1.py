from HTTPHandler import HTTPHandler
import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888


class HTTPServer:
    def __init__(self, server_address, RequestHandlerClass):
        self._server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass

    def serve_forever(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(self._server_address)
                s.listen()
                client_connection, client_address = s.accept()
                with client_connection:
                    self.RequestHandlerClass(client_connection, client_address, self)

    @property
    def server_address(self):
        return self._server_address


if __name__ == '__main__':
    server = HTTPServer((SERVER_HOST, SERVER_PORT), HTTPHandler)
    print('Starting server...')
    server.serve_forever()
