import socket
import threading
from apscheduler.schedulers.background import BackgroundScheduler

BROADCAST_ADDRESS = '255.255.255.255'
BROADCAST_PORT = 3333

REGISTRATION_PORT = 7777
REGISTRATION_ADDRESS = '10.30.13.219'

def register():
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as registration_server:
    registration_server.bind((REGISTRATION_ADDRESS, REGISTRATION_PORT))
    while True:
      message, address = registration_server.recvfrom(1024)
      print(f'{address} registered')

def discover():
  message = f'{REGISTRATION_PORT}'
  with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as broadcast_socket:
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.sendto(message.encode(), (BROADCAST_ADDRESS, BROADCAST_PORT))
    print('broadcasted message')

def main():
  registration_thread = threading.Thread(target=register)
  registration_thread.start()
  scheduler = BackgroundScheduler()
  scheduler.start()
  scheduler.add_job(discover, 'interval', seconds = 5)
  registration_thread.join()
  scheduler.shutdown()

if __name__ == '__main__':
  main()
