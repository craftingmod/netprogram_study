import socket
BUFSIZE = 1024

# TCP Socket
sock = socket.create_connection(("localhost", 2500))

while True:
  msg = input("Message to send:")
  sock.send(msg.encode())
  data = sock.recv(BUFSIZE)
  if not data:
    break
  print("Received Message: %s" % data.decode())

sock.close()