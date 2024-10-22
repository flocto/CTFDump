import requests

encoding = 'x'
url = 'http://readme2.chal.imaginaryctf.org/'
body = 'test'
r = requests.post(url, headers={'Transfxer-Encoding': encoding}, data=body)
print(r.text)