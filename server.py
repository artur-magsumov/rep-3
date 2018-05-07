from http.server import HTTPServer, BaseHTTPRequestHandler
from from_db_to_json import *

class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.end_headers()
        self.wfile.write(read_db())
httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()

