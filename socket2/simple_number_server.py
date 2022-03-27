from socket import *

table = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"}

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", 3500))
sock.listen(5)
print("Waiting...")

while True:
  client, addr = sock.accept()
  print("Connection from", addr)
  while True:
    data = client.recv(1024)
    if not data:
      break

    try:
      rsp = table[data.decode()]
    except:
      client.send("Try again".encode())
    else:
      client.send(rsp.encode())
    pass
  client.close()