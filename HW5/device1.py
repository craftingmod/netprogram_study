from socket import *
import random

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", 7300))
sock.listen(5)

def getSensorData():
  return {
    "temp": random.randint(0, 40),
    "humid": random.randint(0, 100),
    "iilum": random.randint(70, 150),
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