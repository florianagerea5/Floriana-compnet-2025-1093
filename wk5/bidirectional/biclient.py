import socket
import threading

HOST = '127.0.0.1'
PORT = 3333

def handle_server_write(conn):
  while True:
    data = conn.recv(1024)
    print(f'Received {data}')

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    conn.connect((HOST, PORT))
    server_write_thread = threading.Thread(target=handle_server_write, args=(conn, ))
    server_write_thread.start()
    while True:
      line = input('->')
      conn.sendall(line.encode())

if __name__ == '__main__':
  main()