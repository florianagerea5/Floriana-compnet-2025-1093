import socket

def main():
  HOST, PORT = 'localhost', 3333
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    client.sendall(b'Hello world!!!')
    data = client.recv(1024)
    print('received {}'.format(data))

if __name__ == '__main__':
  main()