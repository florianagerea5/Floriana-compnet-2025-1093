import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./serv.pem', 'serv.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
  sock.bind(('127.0.0.1', 3333))
  sock.listen()
  with context.wrap_socket(sock, server_side=True) as ssock:
    conn, addr = ssock.accept()
    data = conn.recv(1024)
    print(data)