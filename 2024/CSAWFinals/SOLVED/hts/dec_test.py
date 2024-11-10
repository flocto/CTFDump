from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
from collections import Counter
from key_gen import derive_key_from_password

header = open('header.txt', 'rb').read()
body = open('body.txt', 'rb').read()

password = 'HP WOLF SECURITY'

key = derive_key_from_password(password).encode()
cipher = AES.new(bytes.fromhex(key.decode()), AES.MODE_ECB)
body = cipher.decrypt(body)

open('flag.bmp', 'wb').write(header + body)
