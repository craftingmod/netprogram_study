import threading
import select
from socket import *

port = 5200
BUFSIZE = 1024

store:dict[str, list[str]] = {}
socks:list[socket] = []

lock = threading.Lock()

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(("", port))
serverSock.listen(10)

socks.append(serverSock)
print(f"Listening on {port}")

while True:
  # Select wait
  r_sock, w_sock, e_sock = select.select(socks, [], [])

  for s in r_sock:
    sock:socket = s
    if sock == serverSock:
      # If server socket
      clientSock, addr = serverSock.accept()
      print(f"Client {addr} is connected.")
      socks.append(clientSock)
    else:
      # P2P Socket (Message send and receive)
      try:
        data = sock.recv(BUFSIZE)
      except:
        # Closed
        sock.close()
        socks.remove(sock)
        continue
      if not data:
        # Also close
        sock.close()
        socks.remove(sock)
        continue

      # Get command
      content = data.decode()
      # Send Command
      if content.startswith("send "):
        postfix = content[5:]
        splt = postfix.find(" ")
        if splt > 0 and splt < len(postfix) - 1:
          mboxID = postfix[0:splt]
          message = postfix[splt + 1:]
          # Find message store
          lock.acquire()
          # === Lock ===
          if mboxID in store:
            store[mboxID].append(message)
          else:
            store[mboxID] = [message]
          # ============
          lock.release()
          print(f"Message \"{message}\" stored in mailbox {mboxID} from {addr}")
          sock.send("OK".encode())
        else:
          sock.send("Invalid Message.".encode())
      elif content.startswith("receive "):
        postfix = content[8:]
        if len(postfix) > 0:
          mboxID = postfix
          sendMsg = None
          # Find message store
          lock.acquire()
          # === Lock ===
          if mboxID in store and len(store[mboxID]) > 0:
            sendMsg = store[mboxID].pop(0)
          # ============
          lock.release()
          if sendMsg == None:
            sock.send("No messages".encode())
          else:
            print(f"Message \"{sendMsg}\" in mailbox {mboxID} sent.")
            sock.send(sendMsg.encode())
        else:
          sock.send("Invalid mailbox ID.".encode())
      elif content.startswith("receive"):
        # just duplication
        sock.send("Invalid mailbox ID.".encode())
      elif content == "quit":
        # Close connection
        print(f"Lost connection from someone.")
        socks.remove(sock)
        sock.close()
      else:
        sock.send("Unknown Command.".encode())
        pass
