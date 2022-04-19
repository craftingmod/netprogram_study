from socket import *
import time

sendAddr = ("127.0.0.1", 2500)
BUFFSIZE = 1024
isDebug = False
maxTry = 3

sock = socket(AF_INET, SOCK_DGRAM)

isFail = True

def printDebug(msg:str):
  if isDebug:
    print(f"# {msg}")


# Send ping
sock.sendto("ping".encode(), sendAddr)
sendTime = time.time()

for i in range(maxTry):
  printDebug(f"Trial {i+1}")
  # 1 sec Timeout
  sock.settimeout(1.0)
  try:
    data, addr = sock.recvfrom(BUFFSIZE)
    if not data:
      continue
    
    msg = data.decode()
    if msg == "pong":
      currentTime = time.time()
      isFail = False
      print(f"Success (RTT: {currentTime - sendTime})")
      break
  except timeout:
    printDebug(f"Packet {i+1} timeout.")
    if i < (maxTry-1):
      printDebug(f"Retrying..")
      sock.sendto("ping".encode(), sendAddr)
      sendTime = time.time()
    
if isFail:
  print("Fail")