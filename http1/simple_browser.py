import requests

url = "http://example.org/"
rsp = requests.get(url)
print(rsp.status_code)
print(rsp.headers)
print(rsp.text)