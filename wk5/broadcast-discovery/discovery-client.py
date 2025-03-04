import socket

# standard discovery broadcast port
PORT = 3333

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as receiver:
    receiver.bind(('', PORT))
    print(f'listening for broadcasts on port {PORT}')

    while True:
      data, address = receiver.recvfrom(1024)
      port = int(data.decode())
      print(f'received registration broadcast for {address}:{port}')
      with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        sender.sendto(b'additional info', (address[0], port))
        print('sent registration message')

if __name__ == '__main__':
  main()