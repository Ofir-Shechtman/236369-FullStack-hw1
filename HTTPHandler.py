from hw1_utils import decode_http
from HTMLBuilder import HTMLBuilder
from enum import Enum
from urllib.parse import urlparse, unquote

PROTOCOL_VERSION = 'HTTP/1.1'
RECV_BUFFER = 4096


class HTTPStatusCodes(Enum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501


class HTTPConnectionError(BaseException):
    def __init__(self, status_code):
        self.status_code = status_code


class HTTPHandler:
    def __init__(self, client_connection, client_address, server):
        self.client_address = client_address
        self.client_connection = client_connection
        self.server = server
        self._headers_buffer = []
        self.wfile = self.client_connection.makefile('wb')
        try:
            self.handle()
        except HTTPConnectionError as e:
            self.send_response(e.status_code)
            self.end_headers()
            self.wfile.flush()
        except Exception:
            self.send_response(HTTPStatusCodes.INTERNAL_SERVER_ERROR)
            self.end_headers()
            self.wfile.flush()
        finally:
            self.wfile.close()

    @property
    def server_address(self):
        return ':'.join(map(str, self.server.server_address))

    def parse_request(self) -> None:
        http_data = self.client_connection.recv(RECV_BUFFER)
        decoded_http = decode_http(http_data)
        request = decoded_http['Request'].split()
        if len(request) != 3:
            raise HTTPConnectionError(HTTPStatusCodes.INTERNAL_SERVER_ERROR)
        self.command, raw_path, request_version = request
        if request_version != PROTOCOL_VERSION:
            raise HTTPConnectionError(HTTPStatusCodes.INTERNAL_SERVER_ERROR)
        self.path = unquote(urlparse(raw_path).path)

    def send_response(self, code):
        """Send the response header only."""
        self._headers_buffer.append(f"{PROTOCOL_VERSION} {code.value} {code.name}\r\n".encode('latin-1', 'strict'))

    def send_header(self, keyword, value):
        """Send a MIME header to the headers buffer."""
        self._headers_buffer.append(f"{keyword}: {value}\r\n".encode('latin-1', 'strict'))

    def end_headers(self):
        """Send the blank line ending the MIME headers."""
        self._headers_buffer.append(b"\r\n")
        self.wfile.write(b"".join(self._headers_buffer))
        self._headers_buffer = []

    def handle(self):
        """Handle multiple requests if necessary."""
        self.parse_request()
        if self.command == 'GET':
            self.do_GET()
        else:
            raise HTTPConnectionError(HTTPStatusCodes.NOT_IMPLEMENTED)
        self.wfile.flush()  # actually send the response if not already done.

    def do_GET(self) -> None:
        message = bytes()
        try:
            if self.path.endswith('.png'):
                message = HTMLBuilder.build_image_page(self.path)
                self.send_response(HTTPStatusCodes.OK)
                self.send_header('Content-Type', 'image/png')
                self.send_header("Accept-Ranges", "bytes")
            else:
                if self.path == '/':
                    message = HTMLBuilder.build_index_page()
                else:
                    message = HTMLBuilder.build_pdf_page(self.path)
                self.send_response(HTTPStatusCodes.OK)
                self.send_header('Content-Type', 'text/html')
        except HTTPConnectionError as e:
            self.send_response(e.status_code)
        except Exception:
            self.send_response(HTTPStatusCodes.NOT_FOUND)
            self.send_header('Content-Type', 'text/html')
            with open(r"error_page\404.html", 'r') as html:
                message = html.read().encode('utf-8')
        finally:
            self.end_headers()
            self.wfile.write(message)
