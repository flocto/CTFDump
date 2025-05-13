import struct
from scipy.interpolate import lagrange

polys = []
for i in range(1, 4):
    fname = f'replica_{i}_test.txt'
    dat = open(fname, 'rb').read()
    polys.append(struct.unpack(f'<{len(dat)//8}q', dat))

# print(polys)

for p1, p2, p3 in zip(*polys):
    print(p1, p2, p3)
    poly = lagrange([1, 2, 3], [p1, p2, p3])
    print(poly)