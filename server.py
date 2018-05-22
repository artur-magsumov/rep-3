#!/usr/bin/env python

"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost:8000
Send a HEAD request::
    curl -I http://localhost:8000
Sending data from file:
    curl --data-binary "@/home/art/MySql_doit/server/goon/client/csv_table.csv" http://localhost:8000/file
"""
from http.server import *
from from_db_to_json import *
from http.client import *
from mysql import *

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_headers()
            self.wfile.write(b"Hi!\nGET-request: /catalog\nPost-request: /file\n")
        elif self.path == '/catalog':
            self._set_headers()
            self.wfile.write(read_db() + b'\n')

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        ##################################################
        if self.path == '/file':
            self._set_headers()
            content_len = int(self.headers['Content-Length'])
            posted_data = self.rfile.read(content_len)
            
            with open("received_file.csv", "w") as f:
                f.write(posted_data.decode("utf8"))

            get_pattern_and_acc_num_from_database()
            open_csv("received_file.csv")
            appending_values_to_acc_num()
            write_new_data_to_csv("received_file.csv")
            
            f = open("received_file.csv", "rb")
            self.wfile.write(f.read())
            f.close()
            return
            
def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
