from http.server import HTTPServer, BaseHTTPRequestHandler

class http_handler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    with open("index.html", "r", encoding="utf-8") as f:
      msg = f.read()
      self.wfile.write(msg.encode("utf-8"))

httpd = HTTPServer(("localhost", 8080), http_handler)
print(f"Serving HTTP on localhost:{httpd.server_port}")
httpd.serve_forever()