import socketserver

class SimpleTcpHandler(socketserver.BaseRequestHandler):
  def handle(self):
    self.data = self.request.recv(1024).strip()
    print('{} wrote {}'.format(self.client_address[0], self.data))
    self.response = self.data.upper()
    self.request.sendall(self.response)

def main():
  HOST, PORT = 'localhost', 3333
  with socketserver.TCPServer((HOST, PORT), SimpleTcpHandler) as server:
    server.serve_forever()

if __name__ == '__main__':
  main()