from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse, request
import requests, json
import cv2
import base64

REST_API_KEY = open("key.txt", "r").read().strip()
TOKEN_API_URL = "https://kauth.kakao.com/oauth/token"
PROFILE_API_URL = "https://kapi.kakao.com/v1/api/talk/profile"
TALK_API_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

BRACKET_LEFT = "{"
BRACKET_RIGHT = "}"

class http_handler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.route()
  
  def route(self):
    parsed_path = parse.urlparse(self.path)
    real_path = parsed_path.path
    if real_path == "/":
      self.send_html()
    elif real_path == "/favicon.svg":
      self.send_favicon()
    elif real_path == "/oauth":
      self.process_oauth()
    elif real_path == "/key":
      self.send_key()
    else:
      self.response(404, "Not Found")

  def send_key(self):
    self.send_response(200)
    self.send_header("Content-Type", "application/json")
    self.end_headers()
    self.wfile.write(f"{BRACKET_LEFT}\"key\":\"{REST_API_KEY}\"{BRACKET_RIGHT}".encode("utf-8"))

  def send_favicon(self):
    self.send_response(200)
    self.send_header("Content-Type", "image/svg+xml")
    self.end_headers()
    with open("favicon.svg", "r") as f:
      self.wfile.write(f.read().encode("ascii"))

  def send_html(self):
    self.send_response(200)
    self.end_headers()
    with open("index_kakao.html", "r", encoding="utf-8") as f:
      msg = f.read()
      self.wfile.write(msg.encode("utf-8"))
  
  def process_oauth(self):
    # 인증 코드 얻기
    parsed_path = parse.urlparse(self.path)
    query = parsed_path.query
    parsed_query = parse.parse_qs(query)
    # 인증 코드
    authorize_code = parsed_query["code"]
    print(f"Authorize Code: {authorize_code}")
    self.response(200, "Kakao authentication is successful.")

    # Access Token과 Refresh Token 얻기
    data = {
      "grant_type": "authorization_code",
      "client_id": REST_API_KEY,
      "redirect_uri": "http://localhost:8888/oauth",
      "code": authorize_code,
    }
    resp = requests.post(TOKEN_API_URL, data=data)
    resp_json = json.loads(resp.text)
    access_token = resp_json["access_token"]
    refresh_token = resp_json["refresh_token"]
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")

    # 카카오톡 프로필 가져오기
    header = {
      "Authorization": f"Bearer {access_token}",
    }
    resp_profile = requests.get(PROFILE_API_URL, headers=header)
    profile_json = resp_profile.json()
    print(profile_json)
    request.urlretrieve(profile_json["profileImageURL"], "profile.png")

    # 프로필 출력
    img = cv2.imread("profile.png")
    cv2.imshow("profile", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 나한테 카톡 보내기
    template_object = {
      "object_type": "text",
      "text": "카카오 API로 메세지 보내기",
      "link": {
        "web_url": "https://example.org",
        "mobile_web_url": "https://m.naver.com"
      }
    }

    template_object_json = json.dumps(template_object)
    data = {
      "template_object": template_object_json,
    }
    resp_talk = requests.post(TALK_API_URL, data=data, headers=header)

  def response(self, status_code, body):
    self.send_response(status_code)
    self.send_header("Content-Type", "text/plain")
    self.end_headers()
    self.wfile.write(body.encode("utf-8"))

if __name__ == "__main__":
  server_address = ("localhost", 8888)
  httpd = HTTPServer(server_address, http_handler)
  print(f"Serving HTTP on {server_address[0]}:{server_address[1]}")
  httpd.serve_forever()