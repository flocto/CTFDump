from Crypto.Cipher import AES

def mainxor(data):
    xorkey = b'\x0d\x15\x5E\x9A\xA1\xCC\xF9'
    out = b''

    for i in range(len(data)):
        j = i * 2 % 7
        c = data[i] ^ xorkey[j]
        out += bytes([c])
    
    return out

#   *(_QWORD *)v63 = 0x3246CC35D70C157CLL;
#   *(_QWORD *)&v63[8] = 0x80DB709C398A2CA1LL;
#   *(_QWORD *)&v63[16] = 0xFC58D32B0DAF2CB9LL;
#   *(_QWORD *)&v63[24] = 0x9652B1B2854899E7LL;

init = [0x3246CC35D70C157C, 0x80DB709C398A2CA1, 0xFC58D32B0DAF2CB9, 0x9652B1B2854899E7]
init = b''.join([x.to_bytes(8, 'little') for x in init])
print(init, len(init))

#  59h ; Y             ; DATA XREF: .data:addkey↓o
# .data:0000000000578369                 db 0C9h
# .data:000000000057836A                 db  86h
# .data:000000000057836B                 db 0BBh
# .data:000000000057836C                 db 0F6h
# .data:000000000057836D                 db  15h
# .data:000000000057836E                 db 0C1h
# .data:000000000057836F                 db  27h ; '
# .data:0000000000578370                 db 0E7h
# .data:0000000000578371                 db  22h 
addkey = b'Y\xC9\x86\xBB\xF6\x15\xC1\'\xE7"'
print(addkey, len(addkey))

key = b''

for i in range(32):
    j = (i * 3) % 10
    c = addkey[i % 10] & 0x1f ^ ((init[i] + addkey[j]) & 0xff)
    key += bytes([c])

enc = bytes.fromhex('8a7e7886aac76f550b3e0bbd59c5f0ea46ed30c858a99423372bbccc960fcf7158a23de05c2788617986affa78ae8b608c6b38386c4715b9e49bcb')
# enc = bytes.fromhex('fc7366f1405874607c70f2bc0a0940573bf2b350c4ff1d3e955a989e323a7e97e58029c5')

enc = mainxor(enc)

nonce_size = 12
tag_size = 16

nonce, enc = enc[:nonce_size], enc[nonce_size:-tag_size]
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=tag_size)

dec = cipher.decrypt(enc)

dec = mainxor(dec)
print(dec)
