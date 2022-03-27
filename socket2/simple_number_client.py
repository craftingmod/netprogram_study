from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("localhost", 3500))

while True:
  msg = input("Number to send (1~10):")
  if msg == "q":
    break
  
  sock.send(msg.encode())

  msg = sock.recv(1024)
  print("Received message:", msg.decode())