import http.server
import socketserver

PORT=8080

handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(('', PORT), handler) as httpd:
  httpd.serve_forever()