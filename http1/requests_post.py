import requests

url = 'https://httpbin.org/post'
data = {'IoT': '2017'}
print(f"{url} with data {data}")
rsp = requests.post(url, data=data)
print(rsp.text)

print(f"{url} with json {data}")
rsp = requests.post(url, json=data)
print(rsp.text)

files = {'file': open('white.png', 'rb')}
print(f"{url} with files {files}")
rsp = requests.post(url, files=files)
print(rsp.text)