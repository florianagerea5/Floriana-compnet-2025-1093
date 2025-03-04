import http.server
import socketserver

PORT=8080

class CustomHTTPHandler(socketserver.StreamRequestHandler):
  def handle(self):
    self.wfile.write('HTTP1.1 200 OK\n\nHello'.encode('utf-8'))

handler = CustomHTTPHandler

with socketserver.TCPServer(('', PORT), handler) as httpd:
  httpd.serve_forever()