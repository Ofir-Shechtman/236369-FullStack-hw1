from http.server import HTTPServer
from HTTPHandler import HTTPHandler

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888

Server = HTTPServer

if __name__ == '__main__':
    server = Server((SERVER_HOST, SERVER_PORT), HTTPHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

