from socket import *
import random

port = 2500
BUFFSIZE = 1024

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("", port))
print(f"# Binded port {port}")

while True:
  msg, addr = sock.recvfrom(BUFFSIZE)
  print(f"# Msg: {msg}, addr: {addr}")
  
  # If not message
  if not msg:
    break

  # If message is ping
  if msg.decode() == "ping":
    # Drop by 50%
    if random.randint(0, 1) == 0:
      print(f"# Message dropped")
      # Drop
      continue
    else:
      print(f"# Pong sent to {addr}")
      sock.sendto("pong".encode(), addr)
  pass

sock.close()