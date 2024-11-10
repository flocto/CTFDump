data = b'\x06\x01\x00\n\x01aD\x06\x01\x00\x0b\x01u4\x06\x01\x00\x0c\x01ib\x06\x01\x00\r\x01lc\x06\x01\x00\x0e\x011e\x06\x01\x00\x0f\x01fi\x06\x01\x00\x10\x01be\x06\x01\x00\x11\x01b0'

data = [data[i+5:i+7][::-1] for i in range(0, len(data), 7)]
data = b''.join(data)

def rol8(n, r):
    return ((n << r) | (n >> (8 - r))) & 0xff

def ror8(n, r):
    return ((n >> r) | (n << (8 - r))) & 0xff

out = b''

for i in range(16):
    d = data[i]
    # 019d: 10 01 ac jnz 0x01ac // if (itr < 0x02) goto 0x01ac
    # 01ab: 06       stores // mem[0x16] = rol8(mem[0x16], 4)
    # 01b4: 10 01 c3 jnz 0x01c3 // if (itr < 0x09) goto 0x01c3
    # 01c2: 06       stores // mem[0x16] = ror8(mem[0x16], 2)
    # 01cb: 10 01 da jnz 0x01da // if (itr < 0x0d) goto 0x01da
    # 01d9: 06       stores // mem[0x16] = rol8(mem[0x16], 7)
    # 01e2: 10 01 f1 jnz 0x01f1 // if (itr < 0x0f) goto 0x01f1
    # 01f0: 06       stores // mem[0x16] = rol8(mem[0x16], 7)
    if i == 2:
        d = rol8(d, 4)
    if i == 9:
        d = ror8(d, 2)
    if i == 0xd:
        d = rol8(d, 7)
    if i == 0xf:
        d = rol8(d, 7)
    out += bytes([d])

print(out)