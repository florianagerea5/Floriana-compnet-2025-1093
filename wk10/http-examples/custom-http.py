import http.server
import socketserver
from os import listdir
from os.path import isfile, join

PORT = 8000

class SimpleHTTPHandler(socketserver.StreamRequestHandler):
  """
  custom http handler
  """
  def handle(self):
    self.data = self.request.recv(1024).strip()
    self.text_data = self.data.decode('utf-8')
    self.parsed_data = self.parse(self.text_data)
  
  def parse(self, data):
    print("{} requested:".format(self.client_address[0]))
    lines = self.text_data.splitlines()
    request_line = lines[0]
    (method, address, version) = request_line.split(' ')
    address = address[1:] if address != '/' else 'index.html'
    print("{} {}".format(method, address))
    onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
    if address in onlyfiles:
      resource = address
      with open(resource, 'r') as f:
        content = f.read()
        content = version + ' 200 OK\n' + 'content-type: text/html\n\n' + content
        self.wfile.write(content.encode('utf-8'))
    else:
      resource = '404.html'
      with open(resource, 'r') as f:
        content = f.read()
        content = version + '404 OK\n' + 'content-type: text/html\n\n' + content
        self.wfile.write(content.encode('utf-8'))


Handler = SimpleHTTPHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
  print("serving at port", PORT)
  httpd.serve_forever() 