from socket import *

port = 5200

store:dict[str, list[str]] = {}

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("", port))
print(f"Listening on port {port}")

while True:
  data, addr = sock.recvfrom(1024)
  
  content = data.decode()
  if content.startswith("send "):
    postfix = content[5:]
    splt = postfix.find(" ")
    if splt > 0 and splt < len(postfix) - 1:
      mboxID = postfix[0:splt]
      message = postfix[splt + 1:]
      # Find
      if mboxID in store:
        store[mboxID].append(message)
      else:
        store[mboxID] = [message]
      print(f"Message \"{message}\" stored in mailbox {mboxID} from {addr}")
      sock.sendto("OK".encode(), addr)
    else:
      sock.sendto("Invalid message.".encode(), addr)
  elif content.startswith("receive "):
    postfix = content[8:]
    if len(postfix) > 0:
      mboxID = postfix
      # Find
      if mboxID in store and len(store[mboxID]) > 0:
        firstmsg = store[mboxID].pop(0)
        print(f"Message \"{firstmsg}\" in mailbox {mboxID} sent to {addr}")
        sock.sendto(firstmsg.encode(), addr)
      else:
        sock.sendto("No messages".encode(), addr)
    else:
      sock.sendto("Invalid mailbox ID.".encode(), addr)
    pass
  elif content == "quit":
    sock.close()
    break
  else:
    sock.sendto("Unknown Command.".encode(), addr)
    pass