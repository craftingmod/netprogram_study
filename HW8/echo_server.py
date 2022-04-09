# MUST BE RUN with UAC in Windows.

import random
import time

from udpsocket import UDPSocket

# Source
source = ("127.0.0.1", 2500)
BUFFSIZE = 1024

# Create socket
sock = UDPSocket(source)

# Chat Server
print("Waiting someone is saying..")
while True:
  firstConn = True
  connIP = ""
  lastTime = time.process_time()
  while True:
    data, addr = sock.receive()
    if not data:
      break

    if firstConn:
      print(f"[Log] Connected with {addr[0]}.")
      firstConn = False
      connIP = addr[0]
    elif connIP != addr[0]:
      if time.process_time() - lastTime > 60:
        print(f"[Log] Switching connection to {addr[0]}.")
        connIP = addr[0]
      else:
        lastTime = time.process_time()
        continue
    
    msg = data.decode()
    print("<- ", msg)
    if msg == "quit":
      break
    msg = input("-> ")
    if len(msg) <= 0:
      msg = "(empty message)"

    sock.connect(addr)
    sock.send(msg.encode("utf8"))

    if msg == "quit":
      break

    lastTime = time.process_time()
    pass
  decision = input("Continue? (y/n):")
  if decision == "n":
    break

sock.close()