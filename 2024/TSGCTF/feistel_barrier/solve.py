from server import mgf, xor, h_len
from pwn import remote, process
# nc 34.146.145.253 10961
n,e,c = 0,0,''
r = remote('34.146.145.253', 10961)
# r = process(['python3', 'server.py'])

n = int(r.recvline_contains(b'n = ').decode().strip().split(' ')[-1])
e = int(r.recvline_contains(b'e = ').decode().strip().split(' ')[-1])
c = bytes.fromhex(r.recvline().decode().strip().split(' ')[-1])
c = int.from_bytes(c, 'big')

fac = pow(3, e, n)
c_2 = (c * fac) % n
c_2 = c_2.to_bytes(128, 'big')
r.sendlineafter(b'ciphertext:', c_2.hex())

ct = bytes.fromhex(r.recvline().decode().strip())
ct = int.from_bytes(ct, 'big')
ct = (ct * (pow(3, -1, n))) % n
ct = ct.to_bytes(128, 'big')
print(ct)
ct = ct[1:]
maskedSeed = ct[:32]
maskedDB = ct[32:]

print(maskedSeed.hex())
print(maskedDB.hex())

seedMask = mgf(maskedDB, h_len)
seed = xor(maskedSeed, seedMask)
print(seed.hex())

dbMask = mgf(seed, len(maskedDB))
DB = xor(maskedDB, dbMask)
print(DB)