from socket import create_connection
from datetime import datetime

print("Connecting Device 1...")
sock1 = create_connection(("localhost", 7300))
print("Connecting Device 2...")
sock2 = create_connection(("localhost", 7301))

def nowDate():
  return datetime.now().strftime("%a %b %d %H:%M:%S %Y")

def dataToLine(data:str):
  if data.startswith(":data"):
    arr = data.split(";")[1:]
    arr = [x.replace(":", "=") for x in arr]
    return ", ".join(arr)
  else:
    return ""

writeData = ""
while True:
  userInput = input("Input data to send: ")
  # Device 1
  if userInput == "1":
    sock1.send("Request".encode())
    data = sock1.recv(1024)
    if not data:
      print("Data is empty.")
      continue
    content = data.decode()
    line = dataToLine(content)
    if len(line) > 0:
      line = f"{nowDate()}: Device1: {line}\n"
      print(f"[Device 1] Received {line}")
      writeData += line
  # Device 2
  elif userInput == "2":
    sock2.send("Request".encode())
    data = sock2.recv(1024)
    if not data:
      print("Data is empty.")
      continue
    content = data.decode()
    line = dataToLine(content)
    if len(line) > 0:
      line = f"{nowDate()}: Device2: {line}\n"
      print(f"[Device 2] Received {line}")
      writeData += line
  # Flush
  elif userInput == "quit":
    # Write
    file = open("data.txt", "w")
    file.write(writeData)
    file.close()
    # Quit
    sock1.send("quit".encode())
    sock2.send("quit".encode())
    sock1.close()
    sock2.close()
    break
