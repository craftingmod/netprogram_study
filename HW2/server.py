import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 8700))
sock.listen(2)

while True:
  client, addr = sock.accept()
  print("Connection from", addr)
  client.send(b"Hello " + addr[0].encode())
  # 학생의 이름을 수신한 후 출력
  msg = client.recv(1024)
  print(msg.decode())
  # 학생의 학번을 전송
  studentnum = 20171531
  client.send(studentnum.to_bytes(4, byteorder="big"))

  client.close()