import socket
import cv2
import numpy as np

BUF_SIZE = 8192
LENGTH = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 5000))

while True:
  sock.send(b"start")

  rx_size = 0
  data = b""
  while rx_size < LENGTH:
    rx_buf = sock.recv(BUF_SIZE)
    if not rx_buf:
      break
    data = data + rx_buf
    rx_size += len(rx_buf)

  if rx_size < LENGTH:
    break

  frame_len = int(data)

  sock.send(b"image")

  rx_size = 0
  byteData = b""
  while rx_size < frame_len:
    rx_buf = sock.recv(BUF_SIZE)
    if not rx_buf:
      break
    byteData = byteData + rx_buf
    rx_size += len(rx_buf)

  if rx_size < frame_len:
    break

  data = np.frombuffer(byteData, dtype=np.uint8)
  # imgDecode = cv2.imdecode(data, 1)
  imgDecode = cv2.imdecode(data, cv2.IMREAD_COLOR)
  cv2.imshow("image", imgDecode)

  if cv2.waitKey(1) & 0xFF == ord("q"):
    break
  pass

sock.close()