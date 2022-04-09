import socket
c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.connect(('127.0.0.1', 2500))
c.send(b'message 1')
c.close()