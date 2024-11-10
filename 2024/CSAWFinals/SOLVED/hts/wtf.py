from Crypto.Cipher import AES

data = b'AAAAAAAAAAAAAAAA'
key = b'AAAAAAAAAAAAAAAA'

cipher = AES.new(key, AES.MODE_ECB)
encrypted = cipher.encrypt(data)
print(encrypted.hex())

data2 = b'AAAAAAAAAAAAAAAB'
cipher = AES.new(key, AES.MODE_ECB)
encrypted2 = cipher.encrypt(data2)
print(encrypted2.hex())