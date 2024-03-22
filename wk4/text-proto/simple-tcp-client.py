import socket

HOST, PORT = 'localhost', 3333

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    while True:
      data = input('type "exit" to exit, otherwise enter your message:\n')
      if data.strip() == 'exit':
        break
      client.sendall(data.encode('utf-8'))
      data = client.recv(1024)
      print(data)

if __name__ == '__main__':
  main()