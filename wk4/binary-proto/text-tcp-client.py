import socket

HOST, PORT = 'localhost', 3333
BUFFER_SIZE = 8

def get_command(command):
  payload = command.strip()
  payload_length = len(payload)
  total_length = len(str(payload_length)) + 1 + payload_length
  return f'{total_length} {payload}'

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    while True:
      data = input('type "exit" to exit, otherwise enter your message:\n')
      if data.strip() == 'exit':
        break
      request = get_command(data).encode('utf-8')
      client.sendall(request)
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
      print(full_data)

if __name__ == '__main__':
  main()