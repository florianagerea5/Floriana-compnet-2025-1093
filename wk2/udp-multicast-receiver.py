import socket
import struct

def main():
  multicast_group = '224.0.0.1'
  server_address = (multicast_group, 3333)

  receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  receiver_socket.bind(server_address)

  group = socket.inet_aton(multicast_group)
  mcast = struct.pack('4sL', group, socket.INADDR_ANY)
  receiver_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mcast)

  while True:
    data, address = receiver_socket.recvfrom(1024)
    print(f'Received: {data.decode()} from {address}')

if __name__ == '__main__':
  main()