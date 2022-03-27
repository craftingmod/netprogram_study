from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("localhost", 13200))

while True:
  msg = input("Input calc formula (Ex. 10 + 20): ")
  if msg == "q":
    try:
      sock.send(b"q")
    except:
      pass
    break

  sock.send(msg.encode())

  data = sock.recv(1024)
  if not data:
    print("Data isn't provided.")
    break

  print("Formula Result:", data.decode())