import socketserver
import inotify.adapters
import threading
import socket

TARGET_DIRECTORY = './server-target'

def file_watch(directory):
  notifier = inotify.adapters.Inotify()
  notifier.add_watch(TARGET_DIRECTORY)
  for event in notifier.event_gen(yield_nones=False):
    (_, type_names, path, filenames) = event
    if len(filenames) == 1 and len(type_names) == 1 and type_names[0] == 'IN_CLOSE_WRITE':
      send_multicast(filenames[0])
    if type_names[0] == 'IN_CLOSE_NOWRITE':
      print('sending copy')
      send_multicast(filenames)

def send_multicast(filename):
  MCAST_GROUP = '224.0.0.1'
  MCAST_PORT = 5001
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
  sock.sendto(filename.encode('utf-8'), (MCAST_GROUP, MCAST_PORT))

class FileTCPHandler(socketserver.BaseRequestHandler):
  def handle(self):
    self.data = self.request.recv(1024).strip()
    filename = self.data.decode()
    print(f'sending -> {filename}')
    with open(f'{TARGET_DIRECTORY}/{filename}', 'rb') as f:
      self.request.sendall(f.read())

def main():
  watch_thread = threading.Thread(target=file_watch, args=(TARGET_DIRECTORY, ))
  watch_thread.start()
  # watch_thread.join()
  FILE_SERVER_HOST = '127.0.0.1'
  FILE_SERVER_PORT = 12345
  with socketserver.TCPServer((FILE_SERVER_HOST, FILE_SERVER_PORT), FileTCPHandler) as server:
    server.serve_forever()

if __name__ == '__main__':
  main()