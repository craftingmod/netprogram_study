from socket import *
import threading

port = 2500
BUFFSIZE = 1024

def recvTask(sock):
  while True:
    try:
      data = sock.recv(BUFFSIZE)
    except:
      break

    if not data:
      break
    print(f"{data.decode()}")

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("127.0.0.1", port))

id = input("ID: ")

sock.send(id.encode())

th = threading.Thread(target=recvTask, args=(sock,))
th.start()

while True:
  msg = input()
  sock.send(msg.encode())
  if msg == "quit":
    break

try:
  sock.close()
except:
  pass