import socket
import ssl

hostname = 'localhost'
context = ssl.create_default_context()
context.load_verify_locations('./serv.pem')

with socket.create_connection((hostname, 3333)) as sock:
  with context.wrap_socket(sock, server_hostname=hostname) as ssock:
    ssock.sendall(b'Secure hello there!')