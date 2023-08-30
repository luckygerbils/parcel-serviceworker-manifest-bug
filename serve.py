#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import ssl
import sys

if len(sys.argv) < 2:
    print("Need certificate file and keyfile to serve HTTPs (and needs to be a valid, not self-signed certificate for service worker to register)")
    exit(1)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(
    certfile=sys.argv[1], 
    keyfile=sys.argv[2])

class DistHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server, directory="dist")

TCPServer.allow_reuse_address = True
httpd = TCPServer(('0.0.0.0', 8443), DistHandler)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
print("Serving on https://0.0.0.0:8443")
httpd.serve_forever()
