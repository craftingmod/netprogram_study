from socket import create_connection
from time import sleep

sock = create_connection(("127.0.0.1", 7777))

# -1 + 1 = 0 (init index)
index = -1
while True:
  index = (index + 1) % 3
  sock.send(f"{index+1}".encode())

  data = sock.recv(1024)
  if not data:
    print("Empty Data")
    continue

  temp = int.from_bytes(data[0:4], "big")
  humid = int.from_bytes(data[4:8], "big")
  lumi = int.from_bytes(data[8:12], "big")

  print(f"Temp={temp}, Humid={humid}, Lumi={lumi}")

  sleep(1)