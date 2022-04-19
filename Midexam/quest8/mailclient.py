from socket import *

port = 5200

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("127.0.0.1", port))

print("Command Type is")
print("\"send mboxId message\" or")
print("\"receive mboxId\" or")
print("\"quit\"")
print("===================")

while True:
  msg = input("Enter the command: ")
  sock.send(msg.encode())
  if msg == "quit":
    break
  data = sock.recv(1024)
  print(data.decode())

sock.close()