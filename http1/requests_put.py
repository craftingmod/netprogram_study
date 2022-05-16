import requests

url = 'https://httpbin.org/put'
data = {'IoT': '2017'}
print(f"{url} with data {data}")
rsp = requests.put(url, data=data)
print(rsp.text)

print(f"{url} with json {data}")
rsp = requests.put(url, json=data)
print(rsp.text)

files = {'file': open('white.png', 'rb')}
print(f"{url} with files {files}")
rsp = requests.put(url, files=files)
print(rsp.text)