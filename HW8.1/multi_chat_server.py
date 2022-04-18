from socket import *
import time
import threading

port = 2500
BUFSIZE = 1024

class UserThread(threading.Thread):
  def __init__(self, conn:socket, id:str, header:str, threads:list):
    threading.Thread.__init__(self)
    self.conn = conn
    self.id = id
    self.header = header
    self.threads = threads

  def run(self):
    while True:
      data = self.conn.recv(BUFSIZE)
      if not data:
        break
      print(f"[time:{time.asctime()};host:{self.header};id:{self.id}] {data.decode()}")
      resp = f"[{self.id}] {data.decode()}"
      # Close socket
      if data.decode() == "quit":
        self.threads.remove(self)
        break
      # Broadcasting message
      for th in self.threads:
        if th != self:
          sock:socket = th.conn
          sock.send(resp.encode())
    # Ensure Close
    self.conn.close()
    print(f"# [{self.header}] User {self.id} is disconnected.")

class ServerThread(threading.Thread):
  def __init__(self, conn:socket, header:str, tlist:list[UserThread]):
    threading.Thread.__init__(self)
    self.conn = conn
    self.header = header
    self.tlist = tlist

  def run(self):
    data = self.conn.recv(BUFSIZE)
    if not data:
      self.conn.close()
      return
    id = data.decode()
    if id is None or id == "":
      self.conn.close()
      return
    th = UserThread(self.conn, id, self.header, self.tlist)
    th.daemon = True
    self.tlist.append(th)
    th.start()


sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", port))
sock.listen(10)
print(f"Listening on localhost:{port}")

threadList:list[UserThread] = []

while True:
  conn, (remotehost, remoteport) = sock.accept()
  print("# Connected by", remotehost, remoteport)
  th = ServerThread(conn, f"{remotehost}/{remoteport}", threadList)
  th.daemon = True
  th.start()