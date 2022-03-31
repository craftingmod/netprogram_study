from socket import *
import random

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", 7301))
sock.listen(5)

def getSensorData():
  return {
    "heartbeat": random.randint(40, 140),
    "steps": random.randint(2000, 6000),
    "cal": random.randint(1000, 4000),
  }

while True:
  print("Waiting Connection..")
  conn, addr = sock.accept()
  print(f"Connected by {addr}")
  while True:
    sensorData = getSensorData()
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
    content = data.decode()
    print(f"Received Content: {content}")
    if content.lower() == "request":
      sendStr = ":data;"

      # Sensor data to string
      for key, value in sensorData.items():
        sendStr += f"{key}:{value};"
      if len(sendStr) >= 1:
        sendStr = sendStr[:-1]

      conn.send(sendStr.encode())
    elif content.lower() == "quit":
      conn.send("Bye".encode())
      break
    else:
      conn.send("Send \"Request\" to get sensor data.".encode())
      continue
  print(f"Closing connection by {addr}")
  conn.close()