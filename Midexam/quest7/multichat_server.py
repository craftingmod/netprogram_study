from socket import *
import time
import selectors

class IdSocket:
  def __init__(self, sock:socket, id:str):
    self.sock = sock
    self.id = id

port = 2500
BUFSIZE = 1024
socks:list[IdSocket] = []
sel = selectors.DefaultSelector()

def accept(sock:socket, mask):
  conn, addr = sock.accept()
  print(f"Connected from {addr}")
  sel.register(conn, selectors.EVENT_READ, read)

def read(conn:socket, mask):
  try:
    data = conn.recv(1024)
  except:
    return
  idFound = False
  id = ""
  # Loop 2 times
  for idsock in socks:
    if idsock.sock == conn:
      idFound = True
      id = idsock.id
      break
  # Register Id..
  if not idFound:
    id = data.decode()
    socks.append(IdSocket(conn, id))
    return
  # Send Message to all
  resp = f"[{id}] {data.decode()}"
  print(f"[time:{time.asctime()};id:{id}] {data.decode()}")
  # If quit, close
  if data.decode() == "quit":
    idsock = None
    for s in socks:
      if s.sock == conn:
        idsock = s
        break
    if idsock != None:
      print(f"{idsock.id} Closed.")
      sel.unregister(conn)
      socks.remove(idsock)
      idsock.sock.close()
    return

  for idsock in socks:
    if idsock.sock != conn:
      try:
        idsock.sock.send(resp.encode())
      except:
        # socks.remove(idsock)
        pass

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", port))
sock.listen(10)
print(f"Listening on localhost:{port}")

sel.register(sock, selectors.EVENT_READ, accept)

while True:
  events = sel.select()
  for key, mask in events:
    callback = key.data
    callback(key.fileobj, mask)