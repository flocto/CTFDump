import base64

enc = 'cQoFRQErX1YAVw1zVQdFUSxfAQNRBXUNAxBSe15QCVRVJ1pQEwd/WFBUAlElCFBFUnlaB1ULByRdBEFdfVtWVA=='

dat = base64.b64decode(enc)
dat = bytearray(dat)

key = b'FlareOn2024'

for i in range(len(dat)):
    dat[i] ^= key[i % len(key)]

print(dat)