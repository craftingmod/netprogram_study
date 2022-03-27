from socket import *
import math as Math

ops = ["*", "+", "/", "-"]

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", 13200))
sock.listen(5)

print("Waiting Client...")

while True:
  client, addr = sock.accept()
  print("Connection from", addr)
  while True:
    data = client.recv(1024)
    if not data:
      break
    msg = data.decode()
    if msg == "q":
      break

    # Get first number to calculate
    print("Input formula:", msg)
    valid = False
    result = 0
    for op in ops:
      if op == "-":
        # Shirink space
        msg = msg.replace(" ", "")
        # Change -- to plus
        msg = msg.replace("--", "+")
        # Check first num is negative
        isFirstNegative = False
        if msg[0] == "-":
          isFirstNegative = True
          msg = msg[1:]
        if msg.find("+") >= 0:
          # Plus parsing
          nums = msg.split("+")
          if nums[0].isdigit() and nums[1].isdigit():
            result = int(nums[0])
            if isFirstNegative:
              result *= -1
            result += int(nums[1])
            valid = True
          # break
          break
        elif msg.find("-") >= 0:
          nums = msg.split("-")
          if nums[0].isdigit() and nums[1].isdigit():
            result = int(nums[0])
            if isFirstNegative:
              result *= -1
            result -= int(nums[1])
            valid = True
          # break
          break
        else:
          continue
      arr = msg.split(op)
      if len(arr) == 2:
        # Check is valid number
        try:
          num1 = int(arr[0].strip())
          num2 = int(arr[1].strip())
        except ValueError:
          break

        # Calculate result
        if op == "*":
          result = num1 * num2
        elif op == "+":
          result = num1 + num2
        elif op == "/":
          if num2 == 0:
            # Invalid operation
            break
          result = num1 / num2
        valid = True
        break
    if valid:
      numstr = str(result)
      if result - Math.floor(result) > 0:
        numstr = str(round(result * 10) / 10)
      client.send(numstr.encode())
    else:
      client.send("Invalid request. Try again.".encode())
    pass

  print("Connection lost from ", addr)
  client.close()