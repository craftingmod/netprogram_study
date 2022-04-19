from socket import *

import threading
import os

BUFSIZE = 1024
serverTitle = "My Web Server"

# HTTP Server
class HTTPServerThread(threading.Thread):
  def __init__(self, sock:socket):
    threading.Thread.__init__(self)
    self.sock = sock

  # make Response Header
  def make_resp_header(code:int, contype:str):
    # Fallback
    fheader = "HTTP/1.1 500 Internal Server Error\r\n"
    if code == 200:
      fheader = "HTTP/1.1 200 OK\r\n"
    elif code == 404:
      fheader = "HTTP/1.1 404 Not Found\r\n"
    elif code == 400:
      fheader = "HTTP/1.1 400 Bad Request\r\n"
    elif code == 500:
      fheader = "HTTP/1.1 500 Internal Server Error\r\n"
    fheader += "Content-Type: " + contype + "\r\n"
    fheader += "\r\n"
    return fheader

  # make HTTP Response
  def make_resp_html(code:int, content:str):
    body = HTTPServerThread.make_resp_header(code, "text/html; charset=utf-8")
    body += content
    return body

  # make Binary Response
  def make_resp_binary(code:int, binaryContent:bytes, contype:str):
    headerBytes = HTTPServerThread.make_resp_header(code, contype).encode()
    bodyBytes = bytearray(headerBytes)
    bodyBytes.extend(binaryContent)
    return bodyBytes
  
  # make Error HTTP Response
  def make_resp_error(code:int, message:str):
     return HTTPServerThread.make_resp_header(code, f"<html><head><title>{serverTitle}</title></head><body><div>{message}</div></body></html>").encode()
  
  # Safe Response
  def respSock(self, data:bytes):
    try:
      self.sock.send(data)
      self.sock.close()
    except:
      print(f"# Socket send error!")

  # Define HTTP Server
  def run(self):
    print(f"# Thread is running..")
    
    try:
      data = self.sock.recv(BUFSIZE)
    except:
      print(f"# Error receiving data.")
      return

    # 1. Check data is not empty
    if not data:
      self.respSock(HTTPServerThread.make_resp_error(400, "Invalid Request"))
      return
    
    msg = data.decode()
    msgarr = msg.split("\n")

    # Split space
    httpheader = msgarr[0].split()
    if len(httpheader) < 3:
      self.respSock(HTTPServerThread.make_resp_error(400, "Invalid Request"))
      return

    # Check valid protocol
    httptype = httpheader[2].strip()
    if httptype != "HTTP/1.1":
      self.respSock(HTTPServerThread.make_resp_error(500, f"Protocol {httptype} doesnt support"))
      return

    # Check valid http method
    httpmethod = httpheader[0].strip()
    if httpmethod != "GET":
      self.respSock(HTTPServerThread.make_resp_error(404, "Not Found"))
      return
    
    # Check Path starts /
    httppath = httpheader[1].strip()
    if not httppath.startswith("/"):
      self.respSock(HTTPServerThread.make_resp_error(404, "Not Found"))
      return

    # Refer / to /index.html
    if httppath == "/":
      httppath = "/index.html"

    httppath = httppath[1:]

    # Send binary or HTTP
    try:
      # html
      if httppath.endswith(".html"):
        print("./static/" + httppath)
        f = open("./static/" + httppath, "rt", encoding="utf8")
        content = f.read()
        f.close()
        self.respSock(HTTPServerThread.make_resp_html(200, content).encode())
      else:
        # Binary
        # Set Content Type
        contentType = "application/octet-stream"
        if httppath.endswith(".png"):
          contentType = "image/png"
        elif httppath.endswith(".jpg"):
          contentType = "image/jpg"
        elif httppath.endswith(".ico"):
          contentType = "image/x-icon"

        f = open("./static/" + httppath, "rb")
        content = f.read()
        f.close()

        self.respSock(HTTPServerThread.make_resp_binary(200, content, contentType))
    except:
      self.respSock(HTTPServerThread.make_resp_error(404, "Not Found"))
    pass


# Create TCP Socket
sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", 8080))
sock.listen(10)

# Listen Clients
while True:
  conn, (remotehost, remoteport) = sock.accept()
  print(f"# Connection from {remotehost}:{remoteport}.")
  th = HTTPServerThread(conn)
  th.daemon = True
  th.start()