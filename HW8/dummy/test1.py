# Server: socket3/udp_echo_server.py
# With protocol id support..?

import socket
import struct
port = 2500
BUFFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
sock.bind(("0.0.0.0", port))

print(f"Listening with port {port}")
while True:
  data, addr = sock.recvfrom(BUFFSIZE)
  print(addr)
  print(struct.unpack("!BBHHHBBH4s4s", data[:20]))

sock.close()