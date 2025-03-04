import socket

GROUP = '224.0.0.1'
PORT = 3333

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sender_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sender_socket.sendto(b'Hello multicast!', (GROUP, PORT))