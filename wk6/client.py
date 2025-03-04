import socket
import sys

from transfer_units import RequestMessage, ResponseMessage, RequestMessageType, ResponseMessageType
from serde import serialize, deserialize

def main():
  if len(sys.argv) < 3:
    print('not enough args')
  else:
    (HOST, PORT) = sys.argv[1:3]
    PORT = int(PORT)
    print(f'connecting to {HOST}:{PORT}')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
      while True:
        data = input('storage -> ')
        items = data.strip().split(' ', 1)
        command = items[0]
        if command == 'connect':
          client_socket.sendto(serialize(RequestMessage(RequestMessageType.CONNECT)), (HOST, PORT))
        elif command == 'list':
          client_socket.sendto(serialize(RequestMessage(RequestMessageType.LIST)), (HOST, PORT))
        elif command == 'send':
          client_socket.sendto(serialize(RequestMessage(RequestMessageType.SEND, items[1])), (HOST, PORT))
        elif command == 'disconnect':
          client_socket.sendto(serialize(RequestMessage(RequestMessageType.DISCONNECT)), (HOST, PORT))
        else:
          print('unknown command')
        message, _ = client_socket.recvfrom(1024)
        print(deserialize(message))

if __name__ == '__main__':
  main()