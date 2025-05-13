enc = bytes.fromhex('62 72 56 55 3f 18 57 19 ed fa d8 da aa a9 b1 8d 33 67 7d 51 70 0a 21 23 c9 af d7')

dec = []
for i, e in enumerate(enc):
    b = i % 16
    dec.append(e ^ (b << 4) ^ b)

print(bytes(dec))