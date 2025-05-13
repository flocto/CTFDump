import requests

url = "http://localhost:20906/"

guess = "TSGCTF{hello_world}"

r = requests.get(url + guess)
print(r.text)