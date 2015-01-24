#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle, Frank Yau
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def get_host_port(self,url):
        port = url.split(":")
        if len(port) == 2:
            return 80
        else:
            port = port[2].split("/")
            return int(port[0])

    def connect(self, host, port=80):
        # use sockets!
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def get_code(self, data):
        code = data.split("\r\n")
        code = code[0].split(" ")
        return int(code[1])

    def get_headers(self,data):
        header = data.split("\r\n\r\n")
        return header[0]

    def get_body(self, data):
        body = data.split("\r\n\r\n")
        return body[1]

    def get_host(self, url):
        host = url.split("/")
        port = host[2].split(":")
        return port[0]

    def get_path(self, url):
        host = url.split("/")
        path = "/"
        for i in range(len(host)):
            if i < 3:
                pass
            else:
                path += host[i] + "/"
        if i > 2:
            path = path[:-1]
        return path

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        host = self.get_host(url)
        port = self.get_host_port(url)
        connection = self.connect(host, port)
        path = self.get_path(url)

        message = "GET " + path + " HTTP/1.1\r\n"
        message += "Host: " + host + "\r\n\r\n"

        connection.send(message)

        response = self.recvall(connection)
        code = self.get_code(response)
        body = self.get_body(response)

        print(code,body)
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        host = self.get_host(url)
        port = self.get_host_port(url)
        connection = self.connect(host, port)
        path = self.get_path(url)

        content = ""
        if args != None:
            content = urllib.urlencode(args)

        message = "POST " + path + " HTTP/1.1\r\n"
        message += "Host: " + host + "\r\n"
        message += "Content-Type: application/x-www-form-urlencoded\r\n"
        message += "Content-Length: " + str(len(content)) +"\r\n\r\n"
        message += content

        connection.send(message)

        response = self.recvall(connection)
        code = self.get_code(response)
        body = self.get_body(response)
        return HTTPRequest(code, body)

    def command(self, command, url, args=None):
        #print(url, command, args)
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
