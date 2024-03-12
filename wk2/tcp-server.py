import socket
import threading

HOST = '127.0.0.1'
PORT = 3333


def handle_client(client):
  with client:
    while is_running:
      if client == None:
        break
      data = client.recv(1024)
      if not data:
        break
      client.sendall(data.upper())

def accept_clients(server):
  while is_running:
    client, address = server.accept()
    print(f'{address} has connected')
    client_thread = threading.Thread(target=handle_client, args=(client, ))
    client_thread.start()

is_running = True

def main():
  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    accept_thread = threading.Thread(target=accept_clients, args=(server, ))
    accept_thread.start()
    while is_running:
      data = input('type "exit" to exit:\n')
      if data.strip() == 'exit':
        is_running = False
  except BaseException as err:
    print(err)
  finally:
    if server:
      server.close()
  

if __name__ == '__main__':
  main()