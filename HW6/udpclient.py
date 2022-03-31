from socket import *

port = 5200

sock = socket(AF_INET, SOCK_DGRAM)
sock.connect(("localhost", port))

print("Message Type is")
print("\"send mboxId message\" or")
print("\"receive mboxId\"")
print("===================")

while True:
  msg = input("Enter the message: ")
  sock.send(msg.encode())
  if msg == "quit":
    break
  data = sock.recv(1024)
  print(data.decode())

sock.close()