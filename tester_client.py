import http.client
import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8888


def send_simple_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        s.sendall(request.encode('utf-8'))
        data = s.recv(1024)
        return data.decode('utf-8')


class TesterClient:
    def __init__(self, request_args):
        conn = http.client.HTTPConnection(SERVER_HOST, SERVER_PORT)
        conn.request(*request_args)
        self.response = conn.getresponse()

    def __str__(self):
        return f"Status: {self.response.status}, Reason: {self.response.reason}"

print(TesterClient(["GET", "/"]))
print(TesterClient(["NOGET", "/"]))
print(TesterClient(["GET", "no_path"]))
print(TesterClient(["NOGET", "no_path"]))
print(send_simple_request("GET / HTTP/1.1"))
print(send_simple_request("GET / HTTP/10.4"))
print(send_simple_request("GET /"))
print(send_simple_request("GET /sample HTTP/1.1"))
print(send_simple_request("GET /sample_dir/sample HTTP/1.1"))
# print(send_simple_request(b"GET /sample_dir/sample HTTP/1.1"))




