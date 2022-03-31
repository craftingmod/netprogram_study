from socket import *
import random
import time

# Port
port = 6710
BUFF_SIZE = 1024

# Input mode
mode = input("Enter mode (Server/Client): ").lower()
if mode == "server":
  FIRST_SAY = False
  print("Starting with SERVER mode..")
elif mode == "client":
  FIRST_SAY = True
  print("Starting with CLIENT mode..")
else:
  print("Invalid mode. Only supports Server, Client.")
  exit()

# UDP Socket Binding & Connecting
sock = socket(AF_INET, SOCK_DGRAM)
dest:str = ""
if FIRST_SAY:
  sock.connect(("localhost", port))
  print(f"Connecting on port {port}")
else:
  sock.bind(("", port))
  print(f"Listening on port {port}")

print("=============================")

while True:
  if FIRST_SAY or len(dest) > 0:
    # Send any message
    msg = input("-> ")
    retry = 0
    while retry <= 3:
      resp = f"{str(retry)} {msg}"
      if len(dest) > 0:
        sock.sendto(resp.encode(), dest)
      else:
        sock.send(resp.encode())
      sock.settimeout(2)

      # Receive
      try:
        data, addr = sock.recvfrom(BUFF_SIZE)
        # Check data exist
        if not data:
          retry += 1
          continue
        dest = addr
        # Check ack
        content = data.decode()
        if content == ":ack":
          print(f"# Received ack from {addr}")
          break
      except timeout:
        retry += 1
        continue
      else:
        retry = 4
        break
    if retry >= 4:
      print("# ack timeout. Closing connection.")
      try:
        if len(dest) > 0:
          sock.sendto(":close".encode(), dest)
        else:
          sock.send(":close".encode())
      except:
        pass
      break
  
  # Receive
  sock.settimeout(None)
  while True:
    data, addr = sock.recvfrom(BUFF_SIZE)
    dest = addr
    if random.random() <= 0.5:
      print("# Data Loss!")
      continue
    else:
      sock.sendto(":ack".encode(), addr)
      print(f"<- {data.decode()}")
      break

# Close
sock.close()