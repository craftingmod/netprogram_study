import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

addr = ("127.0.0.1", 8700)
sock.connect(addr)

msg = sock.recv(1024)
print(msg.decode())

# 본인의 이름을 문자열로 전송
sock.send("Donghyun Lee".encode())
# 본인의 학번을 수신 후 출력
msg = sock.recv(1024)
print(int.from_bytes(msg, byteorder="big"))

sock.close()