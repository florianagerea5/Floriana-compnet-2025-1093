import socket
import sys

def main():
  if len(sys.argv) < 3:
    print('usage: <pyfile> <server> <port>')
  else:
    print(sys.argv[1:3])
    (HOST, PORT) = sys.argv[1:3]
    PORT = int(PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
      client.sendto(b'Hello world!', (HOST, PORT))
      data, address = client.recvfrom(1024)
      print('received {}'.format(data))

if __name__  == '__main__':
  main()