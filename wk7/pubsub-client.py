# https://pastebin.com/U8pAe6c4

import socket
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3333  # The port used by the server

class Request:
  def __init__(self, command = '', params = ''):
    self.type = command
    self.params = params
  def __str__(self):
    return f'''
--------------REQUEST-------------
TYPE: {self.type}
{self.params}
-----------------------------------
    '''

class Response:
  def __init__(self, status, payload):
    self.status = status
    self.payload = payload
  def __str__(self):
    return f'''
--------------RESPONSE-------------
TYPE: {self.status}
{self.payload}
-----------------------------------
    '''
def deserialize(response):
  items = response.decode('utf-8').strip().split(' ', 1)
  if (len(items) > 1):
    return Response(items[0], items[1])
  return Response(items[0], None)

def serialize(request):
  return bytes(str(request.type) + ' ' + request.params, encoding='utf-8')

def handle_server_write(s):
    while True:
        data = s.recv(1024)
        # print(f"Received {data!r}")
        response = deserialize(data)
        print(response)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    server_write_thread = threading.Thread(target=handle_server_write, args=(s,))
    server_write_thread.start()
    while True:
        line = input('>')
        items = line.strip().split(' ', 1)
        request = Request(*items)
        s.sendall(serialize(request))
