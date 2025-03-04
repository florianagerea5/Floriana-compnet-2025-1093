import socket
import threading
import io
import pickle

HOST = '127.0.0.1'
PORT = 3333
BUFFER_SIZE = 8

is_running = True

class Request:
  def __init__(self, command, key, resource = None):
    self.command = command
    self.key = key
    self.resource = resource

class Response:
  def __init__(self, payload):
    self.payload = payload

class State:
  def __init__(self):
    self.resources = {}
    self.lock = threading.Lock()
  def add(self, key, resource):
    self.lock.acquire()
    self.resources[key] = resource
    self.lock.release()
  def remove(self, key):
    self.lock.acquire()
    self.resources.pop(key, None)
    self.lock.release()
  def get(self, key):
    if key in self.resources:
      return self.resources[key]
    return None

state = State()

def process_command(data):
  payload = data[1:]
  stream = io.BytesIO(payload)
  request = pickle.load(stream)
  payload = 'command not recognized, doing nothing'
  if request.command == 'add':
    state.add(request.key, request.resource)
    payload = f'added {request.key}'    
  elif request.command == 'remove':
    state.remove(request.key)
    payload = f'removed {request.key}'
  elif request.command == 'get':
    payload = state.get(request.key)
    if not payload:
      payload = f'{request.key} not found'
  stream = io.BytesIO()
  pickle.dump(Response(payload), stream)
  serialized_payload = stream.getvalue()
  payload_length = len(serialized_payload) + 1
  return payload_length.to_bytes(1, byteorder='big') + serialized_payload

def handle_client(client):
  global is_running
  with client:
    while is_running:
      if client == None:
        break
      data = client.recv(BUFFER_SIZE)
      if not data:
        break
      full_data = data
      message_length = full_data[0]
      remaining = message_length - len(data)
      while remaining > 0:
        data = client.recv(BUFFER_SIZE)
        full_data = full_data + data
        remaining = remaining - len(data)
      response = process_command(full_data)
      client.sendall(response)

def accept_clients(server):
  global is_running
  server.settimeout(0.2)
  while is_running:
    try:
      if server:
        client, address = server.accept()
        print(f'{address} has connected')
        client_thread = threading.Thread(target=handle_client, args=(client, ))
        client_thread.start()
    except (socket.timeout, OSError):
      pass

def main():
  global is_running
  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    accept_thread = threading.Thread(target=accept_clients, args=(server, ))
    accept_thread.start()
    while is_running:
      data = input('type "exit" to exit:\n')
      if data.strip() == 'exit':
        is_running = False
  except BaseException as err:
    print(err)
  finally:
    if server:
      server.close()
  

if __name__ == '__main__':
  main()