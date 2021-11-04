from http.server import BaseHTTPRequestHandler
from hw1_utils import decode_http


class HTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:

        message = """<!DOCTYPE html>
<html>
<body>

<h1>My First Heading</h1>

<p>My first paragraph.</p>

</body>
</html>"""
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/html')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))


