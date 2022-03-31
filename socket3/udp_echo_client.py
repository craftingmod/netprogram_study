import socket
port = 2500
BUFFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
  msg = input("Enter a message:")
  sock.sendto(msg.encode(), ("localhost", port))
  data, addr = sock.recvfrom(BUFFSIZE)
  print("Received message: ", data.decode())
  if msg == "q":
    break

sock.close()