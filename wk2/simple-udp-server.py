import socket

def main():
  HOST, PORT = 'localhost', 3333
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind(('', 3333))
    while True:
      message, address = server.recvfrom(1024)
      server.sendto(message.upper(), address)

if __name__ == '__main__':
  main()