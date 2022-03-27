from socket import *

port = 2500
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', port))
sock.listen(1)

conn, (remotehost, remoteport) = sock.accept()
print("Connected by", remotehost, remoteport)

while True:
  msg = ""
  try:
    data = conn.recv(BUFSIZE)
  except:
    break
  else:
    if not data:
      break
    print("Received Message: ", data.decode())
    msg = data.decode()
  try:
    if msg == "quit":
      conn.send("Bye".encode())
      break
    conn.send(data)
  except:
    break

conn.close()
sock.close()