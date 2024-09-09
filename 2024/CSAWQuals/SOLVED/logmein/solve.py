import requests
from tqdm import tqdm
s = requests.Session()
url = 'https://logmein1.ctf.csaw.io/user'

enc = bytes.fromhex('48674c3731025651282f614a4d541034025e1401604d4355135e1a0438334a0045034d53212d1e1e170d56766f520711256c7049693b')
cookie = {
    'info': enc.hex()
}

# r = s.get(url, cookies=cookie)
# print(r.text)

for i in range(len(enc)):
    dat = enc[:i] + bytes([enc[i] ^ 1]) + enc[i+1:]
    r = s.get(url, cookies={'info': dat.hex()})

    if 'csaw' in r.text:
        print(r.text)
        break
