#!/usr/bin/env sage
import struct, itertools
import random

hx = '{:016x}'.format
vals = list(range(256))
random.shuffle(vals)
template = '6878703c3352582c40505a522c40505e68{}5835{}505a585b75000000000000'
template = 'B00A31D2B2070F05575A31FF4887F20F05{}5835{}505a585b75000000000000'

def xorpairs():
    t = bytes.fromhex('5f580f05')
    for d0 in vals:
        for d1 in vals:
            for d2 in vals:
                for d3 in vals:
                    ds = d0,d1,d2,d3
                    x = ''.join(chr(ds[i]) for i in range(4))
                    y = ''.join(chr(t[i]^^ds[i]) for i in range(4))
                    if all(ord(b) in vals for b in y):
                        yield (x, y)

cnt = 0
for x,y in xorpairs():
    cnt += 1

    shc = template.format(x.encode().hex(), y.encode().hex()).replace(' ','')
    shc = bytes.fromhex(shc)
    # assert all(b in printable for b in shc)

    x = [struct.unpack('<Q', shc[i:i+8].ljust(8,b'\0'))[0] for i in range(0, len(shc), 8)]
    print('\x1b[35m{:6}\x1b[0m  \x1b[33m{}\x1b[0m'.format(cnt, ' '.join(map(hx, x))))
    x = x[:4]

    A = matrix([
            [x0, 1, x1]
            for x0, x1 in zip(x, x[1:])
        ])

    for d in A.det().divisors():
        if max(x) < d < 2**64:
            m = d
            break
    else:
        continue

    print('        m = \x1b[34m{}\x1b[0m'.format(hx(m)))

    r = vector(A[:,-1])
    A = A.change_ring(Zmod(m))[:,:2]

    try:
        a, b = A.solve_right(r)
    except ValueError:
        continue
    if not a.is_unit():
        continue

    assert a * x[0] + b == x[1]
    assert a * x[1] + b == x[2]
    assert a * x[2] + b == x[3]
    nxt = ZZ(a * x[3] + b)
    # if nxt & 0xff > 16 or not (nxt & 1):
    #     continue

    print('        a = \x1b[34m{}\x1b[0m'.format(hx(ZZ(a))))
    print('        b = \x1b[34m{}\x1b[0m'.format(hx(ZZ(b))))

    y = (x[0] - b) / a

    out = b''
    for shc in x:
        out += struct.pack('<Q', shc)
    out += struct.pack('<Q', nxt)

    print('        out: \x1b[32m{}\x1b[0m'.format(out.hex()))

    m,a,b,y = map(ZZ,(m,a,b,y))
    print('    --> \x1b[36m{}\x1b[0m'.format(' '.join(map('{:#018x}'.format, (m, a, b, y)))))
    print('        next: \x1b[31m{}\x1b[0m'.format(hx(nxt)))
    # print('    --> \x1b[32m{}\x1b[0m'.format(struct.pack('<QQQQ', m, a, b, y).hex()))

    break