import socket
import threading

HOST = '127.0.0.1'
PORT = 3333
BUFFER_SIZE=8

is_running = True

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
  items = data.split(' ')
  command, key = items[1:3]
  resource = ''
  if len(items) > 3:
    resource = ' '.join(items[3:])
  payload = 'command not recognized, doing nothing'
  if command == 'add':
    state.add(key, resource)
    payload = f'added {key}'    
  elif command == 'remove':
    state.remove(key)
    payload = f'removed {key}'
  elif command == 'get':
    payload = state.get(key)
    if not payload:
      payload = f'{key} not found'
  payload_length = len(payload)
  message_length = len(str(payload_length)) + 1 + payload_length
  # add somekey i'm a little teapot
  return f'{message_length} {payload}'

def handle_client(client):
  global is_running
  with client:
    while is_running:
      if client == None:
        break
      data = client.recv(BUFFER_SIZE)
      data = data.decode('utf-8')
      if not data:
        break
      full_data = data
      message_length = int(data.split(' ')[0])
      remaining = message_length - len(data)
      while remaining > 0:
        data = client.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
        full_data = full_data + data
        remaining = remaining - len(data)
      response = process_command(full_data)
      client.sendall(response.encode('utf-8'))

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