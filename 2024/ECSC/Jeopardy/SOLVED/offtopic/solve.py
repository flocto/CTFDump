#!/usr/bin/env python3

from Crypto.PublicKey.ECC import EccPoint
from Crypto.Random import random
from tqdm import trange
import json
import os
from pwn import remote, proc00ess
# nc offtopic.challs.jeopardy.ecsc2024.it 47013
r = remote('offtopic.challs.jeopardy.ecsc2024.it', 47013)
# r = process('./offtopic.py')

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
G = EccPoint(Gx, Gy)
H = None

class Ciphertext:
    def __init__(self, value):
        self.R = value[0]
        self.S = value[1]

    @classmethod
    def from_pt(cls, m):
        r = random.randint(0, q-1)
        R = r*G
        S = r*H + m*G
        return cls([R, S])

    def __add__(self, other):
        if isinstance(other, int):
            return self + Ciphertext.from_pt(other)
        rand = Ciphertext.from_pt(0)
        return Ciphertext([self.R+other.R+rand.R, self.S+other.S+rand.S])

    def __rmul__(self, other):
        if not isinstance(other, int):
            raise NotImplementedError
        rand = Ciphertext.from_pt(0)
        return Ciphertext([rand.R + other*self.R, rand.S + other*self.S])
    
    def __neg__(self):
        return Ciphertext([-self.R, -self.S])

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        if isinstance(other, int):
            return Ciphertext.from_pt(other) - self
        
# K = 2
# H = K*G
H = -G

r.sendlineafter(b'public key: ', json.dumps({"Hx": int(H.x), "Hy": int(H.y)}).encode())

m = 20
C = Ciphertext.from_pt(m)
C_data = {"Rx": int(C.R.x), "Ry": int(C.R.y), "Sx": int(C.S.x), "Sy": int(C.S.y)}

precomp = {}

for m0 in range(10):
    for m1 in range(10):
        res = m0 * (1-C) + m1 * C
        T = res.R + res.S
        # print(m0, m1, T.x)
        # if int(T.x) in precomp:
        #     print('collision', m0, m1, precomp[int(T.x)])
        precomp[int(T.x)] = (m0, m1)

for i in trange(128):
    r.sendlineafter(b'choice bit: ', json.dumps(C_data).encode())
    data = json.loads(r.recvline().strip().decode())

    R = EccPoint(data["Rx"], data["Ry"])
    S = EccPoint(data["Sx"], data["Sy"])

    # m0, m1 = data['m0'], data['m1']
    # print(m0, m1)

    T = R + S

    if int(T.x) in precomp:
        # print(precomp[int(T.x)])
        r.sendline(json.dumps({"m0": precomp[int(T.x)][0], "m1": precomp[int(T.x)][1]}).encode())

r.interactive()

# for i in range(100):
#     if T == i*G:
#         print(i)
#     if T == i*H:
#         print('-', i)