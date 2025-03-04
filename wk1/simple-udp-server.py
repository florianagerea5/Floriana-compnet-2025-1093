import socket
import sys

def main():
  if (len(sys.argv) < 2):
    print('not enough args')
  else:
    PORT = int(sys.argv[1])
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
      server.bind(('', PORT))
      while True:
        data, address = server.recvfrom(1024)
        server.sendto(data.upper(), address)

if __name__ == '__main__':
  main()