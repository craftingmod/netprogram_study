# MUST BE RUN with UAC in Windows.

import random

from udpsocket import UDPSocket

# Source, Dest
source = ("127.0.0.1", random.randint(17100, 17900))
dest = ("127.0.0.1", 2500)
BUFFSIZE = 1024

# Create socket
sock = UDPSocket(source)
sock.connect(dest)

# Chat Client
while True:
  msg = input("-> ")
  if len(msg) <= 0:
    print(": Try again.")
    continue

  sock.send(msg.encode("utf8"))

  if msg == "quit":
    break
  
  data, addr = sock.receive()
  if not data:
    break

  msg = data.decode()
  print("<- ", msg)
  if msg == "quit":
    break

sock.close()