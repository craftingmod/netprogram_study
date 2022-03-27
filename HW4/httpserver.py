from socket import *
import os

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(("", 12300))
sock.listen(10)
print("Waiting...")

def make_response_header(code:int, contype:str):
  fheader = "HTTP/1.1 404 Not Found\r\n"
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

def make_response(code:int, content:str):
  body = make_response_header(code, "text/html; charset=utf-8")
  body += content
  return body

def make_error(code:int, content:str):
  return make_response(code, f"<html><head><title>{content}</title></head><body><div>{content}</div></body></html>").encode()

while True:
  client, addr = sock.accept()
  print("Connection from", addr)

  data = client.recv(1024)

  # Check not data
  if not data:
    try:
      client.send(make_error(400, "Invalid Request"))
      client.close()
    except:
      pass
    continue
  msg = data.decode()
  msgarr = msg.split("\n")

  # Check empty data
  if len(msgarr) <= 0:
    client.send(make_error(400, "Invalid Request"))
    client.close()
    continue

  # Split space
  httpheader = msgarr[0].split(" ")
  
  # Check header is less than 3
  if len(httpheader) < 3:
    client.send(make_error(400, "Invalid Request"))
    client.close()
    continue

  # Check valid http message
  httptype = httpheader[2].strip()
  if httptype != "HTTP/1.1":
    print("Not valid http type:", httptype)
    client.send(make_error(500, "Protocol does not support"))
    client.close()
    continue

  # Check valid http method
  httpmethod = httpheader[0].strip()
  if httpmethod != "GET":
    print("Not valid http method:", httpmethod)
    client.send(make_error(404, "Not Found"))
    client.close()
    continue

  # Check Path
  httppath = httpheader[1].strip()
  if not httppath.startswith("/"):
    client.send(make_error(404, "Not Found"))
    client.close()
    continue

  # Refer to index.html
  if httppath == "/":
    httppath = "/index.html"

  httppath = httppath[1:]

  try:
    if httppath.endswith(".html"):
      f = open("./static/" + httppath, "rt")
      content = f.read()
      f.close()
      client.send(make_response(200, content).encode())
    else:
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
      bytesHeader = bytearray(make_response_header(200, contentType).encode())
      bytesHeader.extend(content)
      client.send(bytesHeader)
  except:
    client.send(make_error(404, "Not Found"))
    client.close()
    continue
  # Fallback
  client.close()