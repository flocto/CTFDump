import struct

polys = []
for i in range(1, 4):
    fname = f'replica_{i}_challenge.bin'
    dat = open(fname, 'rb').read()
    polys.append(struct.unpack(f'<{len(dat)//8}q', dat))

out = []
for p1, p2, p3 in zip(*polys):
    b = p1 * 2 - p2
    out.append(b)

open('challenge.bin', 'wb').write(bytes(out))

# flag
import subprocess
print(subprocess.check_output(['./challenge.bin']).decode())