# 00007FF64F4D5DF0  9B 36 C0 C3 0A 8F C1 B5 C1 A8 00 DC 75 04 B2 6A  .6ÀÃ..ÁµÁ¨.Üu.²j  
# 00007FF64F4D5E00  9C 4C 40 51 2A 05 EE 32 CA C6 DC E9 0E E7 F5 95  .L@Q*.î2ÊÆÜé.çõ.  
# 00007FF64F4D5E10  B1 5D 5C 6F DF 8E BF 10 1D FB 3C 79 88 2F 83 26  ±]\oß.¿..û<y./.&  
# 00007FF64F4D5E20  2E 34 EE C2 11 06 E6 78 85 60 1B 2C C2 D8 0E 7A  .4îÂ..æx.`.,ÂØ.z  
# 00007FF64F4D5E30  6C B8 21 AD 04 A4 C8 58 41 F7 7C 03 28 AB 08 64  l¸!..¤ÈXA÷|.(«.d  

enc = bytes.fromhex('9B 36 C0 C3 0A 8F C1 B5 C1 A8 00 DC 75 04 B2 6A  9C 4C 40 51 2A 05 EE 32 CA C6 DC E9 0E E7 F5 95 B1 5D 5C 6F DF 8E BF 10 1D FB 3C 79 88 2F 83 26 2E 34 EE C2 11 06 E6 78 85 60 1B 2C C2 D8 0E 7A 6C B8 21 AD 04 A4 C8 58 41 F7 7C 03 28 AB 08 64')

# 0000025D6040F230  71 A4 0C 83 A7 54 7A 2F 39 43 70 8C 3D D1 35 A5  q¤..§Tz/9Cp.=Ñ5¥  
# 0000025D6040F240  0B BC 0C AB 91 AE 0A 3C 9B 8B FD C0 3E 1E 52 F1  .¼.«.®.<..ýÀ>.Rñ  

key1 = b'AttackOnTitan'

# print(len(enc), len(key))

# 0000020F9740DB08  54 68 65 57 6F 72 6C 64 49 73 43 72 75 65 6C 41  TheWorldIsCruelA  
# 0000020F9740DB18  6E 64 4D 65 72 63 69 6C 65 73 73 2E 2E 2E 2E 2E  ndMerciless.....  

key = b'TheWorldIsCruelAndMerciless.....'

# 0000020F9740DBB8  42 75 74 41 6C 73 6F 42 65 61 75 74 69 66 75 6C  ButAlsoBeautiful  
iv = b'ButAlsoBeautiful'

enc = bytes([enc[i] ^ key1[i % len(key1)] for i in range(len(enc))])

print(enc)

from Crypto.Cipher import AES

cipher = AES.new(key, AES.MODE_CBC, iv)
dec = cipher.decrypt(enc)
print(dec)
