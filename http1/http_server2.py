from http.server import HTTPServer, BaseHTTPRequestHandler

class http_handler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"<h1>Hello, IoT!</h1>")

httpd = HTTPServer(("localhost", 8080), http_handler)
print(f"Serving HTTP on localhost:{httpd.server_port}")
httpd.serve_forever()