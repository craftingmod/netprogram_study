import socket
port = int(input("Port No:"))

address = ("127.0.0.1", port)
BUFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(address)

while True:
  msg = input("Message to send: ")
  sock.send(msg.encode())

  data = sock.recv(BUFSIZE)
  datastr = data.decode()
  if datastr == "Bye":
    break
  print("Received Message: ", datastr)

sock.close()