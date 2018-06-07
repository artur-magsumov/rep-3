import os
#import posixpath
import http.server
import urllib.request, urllib.parse, urllib.error
from urllib.request import urlretrieve
import cgi
import shutil
import mimetypes
import re
import requests
from io import BytesIO
from http.server import *
from from_db_to_json import *
from http.client import *
from mysql import *
from my_routes.routes import *
import cgi


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        Тут у меня пути.
        / -- главная
        /catalog -- выводится на экран прошедший
                    валидацию json сформированый из mysql
        /file -- тут можно загрузить csv файлик с таблицей,
                 в которой есть незаполненные поля. Сравнив
                 с БД сервер выдаст в ответ новый csv где
                 все поля уже заполнены
        /любая_другая_страничка -- пытается вывести в окно браузера содержимое
                                   файла если тот существetn (например ссылка
                                   0.0.0.0:8000/server.py) либо выдает а-ля 404
                                   если такого файла не существует. Только что
                                   понял что это, вероятно, уязвимость.
        '''
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(home_page.encode('utf8'))
        elif self.path == '/catalog':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(read_db())
        elif self.path == '/file':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
            self.wfile.write(("<html>\n<title>Upload page </title>\n").encode())
            self.wfile.write(("<body>\n<h2>Upload page </h2>\n").encode())
            self.wfile.write(b"<hr>\n")
            self.wfile.write(b"<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
            self.wfile.write(b"<input name=\"file\" type=\"file\"/>")
            self.wfile.write(b"<input type=\"submit\" value=\"upload\"/></form>\n")
            self.wfile.write(b"<hr>\n<ul>\n")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            filename = self.path[1:]
            try:
                with open(filename, 'rb') as ff:
                    self.copyfile(ff, self.wfile)
            except FileNotFoundError:
                self.wfile.write(b'Page not found')
                self.wfile.write((r"<br><a href='http://0.0.0.0:8000'>main</a>").encode())
                
    def do_POST(self):
        """Serve a POST request."""
        f = BytesIO()
        try:
            r, info, fn = self.deal_post_data()
        except ValueError:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'File is not loaded')
            self.wfile.write(("<br><a href=\"%s\">back</a>" % self.headers['referer']).encode())
            print(self.headers)
            return
        name = fn.split('/')[-1]
        try:
            main_mysql(name)
        except:
            f.write(b'File process is failed :(')
            f.write(("<br><a href=\"%s\">back</a>" % self.headers['referer']).encode())
        
        print((r, info, "by: ", self.client_address))
        
        f.write(b'<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write(b"<html>\n<title>Upload Result Page</title>\n") # Имя вкладки
        f.write(b"<body>\n<h2>Upload Result Page</h2>\n")       # Хэд страницы
        f.write(b"<hr>\n")
        if r:
            f.write(b"<strong>Success:</strong>")
        else:
            f.write(b"<strong>Failed:</strong>")
        f.write(info.encode())
        f.write(("<br><a href=\"%s\">back</a>" % self.headers['referer']).encode())
        f.write(('<li><a href="%s" download>%s</a>\n'
                    % (urllib.parse.quote(fn.split('/')[-1]), cgi.escape(fn.split('/')[-1]))).encode())
        f.write(cgi.escape(fn.split('/')[-1]).encode())
        
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
    def process_file(filename):
        get_pattern_and_acc_num_from_database()
        open_csv(filename)
        appending_values_to_acc_num()
        write_new_data_to_csv(filename)
        
    def deal_post_data(self):
        content_type = self.headers['content-type']
        # (см выше)multipart/form-data; boundary=----WebKitFormBoundaryAeZ2KCQnBIPX9OC5
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        print(remainbytes, '-----')
        print(self.headers)
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line.decode())
        if not fn:
            return (False, "Can't find out file name...")
        path = os.getcwd()
        fn = os.path.join(path, fn[0]) #соединяет пути с учетом особенностей ОС
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                return (True, "File '%s' upload success!" % fn, fn)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

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
