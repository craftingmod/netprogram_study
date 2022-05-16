import requests
rsp = requests.get('https://example.org')
print(rsp.status_code) # 응답 상태 코드
print(rsp.encoding) # 응답 데이터의 인코딩 방식


url = 'https://search.naver.com/search.naver'
payload = {'query': 'IoT'}
rsp = requests.get(url, params=payload)
print(rsp.url) # 요청 URL
print(rsp.headers) # 응답 헤더
print(rsp.text[:1000]) # 응답 데이터