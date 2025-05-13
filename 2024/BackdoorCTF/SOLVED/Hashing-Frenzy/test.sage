from Crypto.Util.number import *
from pwn import remote
# nc 34.42.147.172 8007
import hashlib
import random

class testhash:
    def __init__(self, data):
        self.data = data

    def digest(self):
        return self.data 

## more hashes, more security
hashes = []
hashes.append(testhash) 
hashes.append(hashlib.md5)
hashes.append(hashlib.sha224)
hashes.append(hashlib.sha256)
hashes.append(hashlib.sha3_224)
hashes.append(hashlib.sha3_256)

def get_hashes(msg):
    return [bytes_to_long(h(msg).digest()) for h in hashes]


r = remote('34.42.147.172', '8007')
r.recvline_contains(b'sample message.')
flag = eval(r.recvline().decode().strip())

r.sendlineafter(b'Enter your choice: ', b'1')
r.sendlineafter(b'to be signed: ', b'a')
c1 = eval(r.recvline().decode().strip())

r.sendlineafter(b'Enter your choice: ', b'1')
r.sendlineafter(b'to be signed: ', b'a')
c2 = eval(r.recvline().decode().strip())
r.close()

hs = get_hashes(b'a')

s1 = sum([c1[i] * hs[i] for i in range(len(hs))]) - c1[-1] 
s2 = sum([c2[i] * hs[i] for i in range(len(hs))]) - c2[-1]

p = int(gcd(s1, s2))
i = 2
while not isPrime(p):
    while p % i == 0:
        p //= i
    p = int(p)
    i += 1

p = int(p)
print(p, p.bit_length())

P = GF(p)

mat = [
    [1, 0, 0, 0, 0, 0, 0, flag[0]],
    [0, 1, 0, 0, 0, 0, 0, flag[1]],
    [0, 0, 1, 0, 0, 0, 0, flag[2]],
    [0, 0, 0, 1, 0, 0, 0, flag[3]],
    [0, 0, 0, 0, 1, 0, 0, flag[4]],
    [0, 0, 0, 0, 0, 1, 0, flag[5]],
    [0, 0, 0, 0, 0, 0, 1, -flag[6]],
    [0, 0, 0, 0, 0, 0, 0, p],
]
mat = Matrix(ZZ, mat)
print('starting lll')
mat = mat.LLL()

for row in mat:
    row = [abs(x) for x in row]
    if row[-2] == 1:
        print(long_to_bytes(row[0]))
