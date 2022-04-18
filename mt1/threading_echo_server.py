from socket import *
import threading

port = 2500
BUFSIZE = 1024

def echoTask(sock:socket, header:str):
  while True:
    data = sock.recv(BUFSIZE)
    if not data:
      break
    print(f"[{header}]Received Message: {data.decode()}")
    sock.send(data)
  sock.close()

class ClientThread(threading.Thread):
  def __init__(self, conn:socket, header:str):
    threading.Thread.__init__(self)
    self.conn = conn
    self.header = header
  def run(self):
    echoTask(self.conn, self.header)

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", port))
sock.listen(5)

while True:
  conn, (remotehost, remoteport) = sock.accept()
  print("Connected by", remotehost, remoteport)
  # th = threading.Thread(target=echoTask, args=(conn, f"{remotehost}:{remoteport}"))
  th = ClientThread(conn, f"{remotehost}:{remoteport}")
  th.start()