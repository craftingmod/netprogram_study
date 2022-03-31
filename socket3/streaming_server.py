import socket
import cv2
import numpy as np

BUF_SIZE = 8192
LENGTH = 10
videoFile = "test.mp4"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 5000))
sock.listen(5)

while True:
  csock, addr = sock.accept()
  print("Client is connected")
  cap = cv2.VideoCapture(videoFile)

  while cap.isOpened():
    ret, frame = cap.read()
    if ret:
      frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      frame = np.asarray(frame, dtype=np.uint8)
      frame = frame.tobytes()
      csock.send(str(len(frame)).ljust(LENGTH).encode())

      temp = csock.recv(BUF_SIZE)
      if not temp:
        break

      csock.send(frame)
    else:
      break
  
  cap.release()
  cv2.destroyAllWindows()
  csock.close()