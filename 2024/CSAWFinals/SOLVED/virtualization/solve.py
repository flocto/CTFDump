def ror(n, x):
    return (n >> x) | (n << (64 - x)) & 0xFFFFFFFFFFFFFFFF

ns = [ 0xe145c86788e5048e, 0xc50728c76468e788, 0x8220628002c08281]

for n in ns[::-1]:
    n ^= 0x5a5a5a5a5a5a5a5a
    n = ror(n, 5)
    n ^= 0xa5a5a5a5a5a5a5a5
    print(n.to_bytes(8, 'little').decode(), end='')