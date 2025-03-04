import socket
import io
import pickle

HOST, PORT = 'localhost', 3333
BUFFER_SIZE = 8

class Request:
  def __init__(self, command, key, resource = None):
    self.command = command
    self.key = key
    self.resource = resource

class Response:
  def __init__(self, payload):
    self.payload = payload


def get_command(command):
  c = command.strip()
  items = c.split(' ')
  request = Request(items[0], items[1], ' '.join(items[2:]))
  stream = io.BytesIO()
  pickle.dump(request, stream)
  serialized_payload = stream.getvalue()
  payload_length = len(serialized_payload) + 1
  return payload_length.to_bytes(1, byteorder='big') + serialized_payload

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    while True:
      data = input('type "exit" to exit, otherwise enter your message:\n')
      if data.strip() == 'exit':
        break
      request = get_command(data)
      client.sendall(request)
      data = client.recv(BUFFER_SIZE)
      if not data:
        break
      full_data = data
      message_length = data[0]
      remaining = message_length - len(data)
      while remaining > 0:
        data = client.recv(BUFFER_SIZE)
        full_data = full_data + data
        remaining = remaining - len(data)
      stream = io.BytesIO(full_data[1:])
      response = pickle.load(stream)
      print(response.payload)

if __name__ == '__main__':
  main()