from MyTCPServer import TCPServer

port = 2500
BUFSIZE = 1024

sock = TCPServer(port)
conn, addr = sock.accept()

print("Connected by", addr)

while True:
  data = conn.recv(BUFSIZE)
  if not data:
    break
  print("Received message:", data.decode())
  conn.send(data)

conn.close()