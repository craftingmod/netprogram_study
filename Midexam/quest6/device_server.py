from socket import *
import random

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", 7777))
sock.listen(5)

def getSensorData():
  return {
    "temp": random.randint(1, 50),
    "humid": random.randint(1, 100),
    "lumi": random.randint(1, 150),
  }

while True:
  print("Waiting Connection..")
  conn, addr = sock.accept()
  print(f"Connected by {addr}")
  while True:
    try:
      data = conn.recv(1024)
    except:
      print("Exception")
      break
    else:
      pass

    if not data:
      print(f"Unexpected Data.")
      break

    sensorData = getSensorData()
    content = data.decode()
    
    sendPacket = bytearray()
    if content == "1":
      sendPacket.extend(sensorData["temp"].to_bytes(4, "big"))
    else:
      sendPacket.extend((0).to_bytes(4, "big"))

    if content == "2":
      sendPacket.extend(sensorData["humid"].to_bytes(4, "big"))
    else:
      sendPacket.extend((0).to_bytes(4, "big"))

    if content == "3":
      sendPacket.extend(sensorData["lumi"].to_bytes(4, "big"))
    else:
      sendPacket.extend((0).to_bytes(4, "big"))
    
    conn.send(sendPacket)

  print(f"Closing connection by {addr}")
  conn.close()