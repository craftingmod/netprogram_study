import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("", 9300))
sock.listen(5)

while True:
  client, addr = sock.accept()
  print("Connection From", addr)

  client.send(time.ctime(time.time()).encode())
  client.close()