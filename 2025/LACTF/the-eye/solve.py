from pwn import remote
# nc chall.lac.tf 31313
r = remote('chall.lac.tf', 31313)

buf = r.recvline()[:-1]
buf = bytearray(buf)
n = len(buf)

from ctypes import CDLL
libc = CDLL('libc.so.6')
seed = libc.time(0)
libc.srand(seed)

rand = []
for i in range(22):
    for _ in range(n):
        rand.append(libc.rand())

rand = rand[::-1]
rand = iter(rand)
for _ in range(22):
    for i in range(n):
        idx = next(rand) % (i + 1)
        a = buf[i]
        buf[i] = buf[idx]
        buf[idx] = a

print(buf)