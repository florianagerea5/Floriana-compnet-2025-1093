import socket
import struct
import sys

MCAST_GROUP = '224.0.0.1'
MCAST_PORT = 5001
# TARGET_DIRECTORY = './client-target'

FILE_SERVER = '127.0.0.1'
FILE_PORT = 12345

def main():
  if len(sys.argv) < 2:
    print('you have to specify a folder')
    exit(0)
  TARGET_DIRECTORY = sys.argv[1]
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind((MCAST_GROUP, MCAST_PORT))

  group = socket.inet_aton(MCAST_GROUP)
  mreq = struct.pack('4sL', group, socket.INADDR_ANY)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

  while True:
    data, address = sock.recvfrom(1024)
    filename = data.decode()
    print(f'{filename} has changed')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((FILE_SERVER, FILE_PORT))
      s.sendall(filename.encode('utf-8'))
      data = s.recv(1024)
      full_data = data
      while data:
        data = s.recv(1024)
        if not data:
          break
        full_data += data
      with open(f'{TARGET_DIRECTORY}/{filename}', 'wb') as f:
        f.write(full_data)

if __name__ == '__main__':
  main()