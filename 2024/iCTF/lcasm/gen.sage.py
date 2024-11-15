

# This file was *autogenerated* from the file gen.sage
from sage.all_cmdline import *   # import sage library

_sage_const_256 = Integer(256); _sage_const_4 = Integer(4); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_8 = Integer(8); _sage_const_2 = Integer(2); _sage_const_64 = Integer(64); _sage_const_3 = Integer(3)#!/usr/bin/env sage
import struct, itertools
import random

hx = '{:016x}'.format
vals = list(range(_sage_const_256 ))
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
                    x = ''.join(chr(ds[i]) for i in range(_sage_const_4 ))
                    y = ''.join(chr(t[i]^ds[i]) for i in range(_sage_const_4 ))
                    if all(ord(b) in vals for b in y):
                        yield (x, y)

cnt = _sage_const_0 
for x,y in xorpairs():
    cnt += _sage_const_1 

    shc = template.format(x.encode().hex(), y.encode().hex()).replace(' ','')
    shc = bytes.fromhex(shc)
    # assert all(b in printable for b in shc)

    x = [struct.unpack('<Q', shc[i:i+_sage_const_8 ].ljust(_sage_const_8 ,b'\0'))[_sage_const_0 ] for i in range(_sage_const_0 , len(shc), _sage_const_8 )]
    print('\x1b[35m{:6}\x1b[0m  \x1b[33m{}\x1b[0m'.format(cnt, ' '.join(map(hx, x))))
    x = x[:_sage_const_4 ]

    A = matrix([
            [x0, _sage_const_1 , x1]
            for x0, x1 in zip(x, x[_sage_const_1 :])
        ])

    for d in A.det().divisors():
        if max(x) < d < _sage_const_2 **_sage_const_64 :
            m = d
            break
    else:
        continue

    print('        m = \x1b[34m{}\x1b[0m'.format(hx(m)))

    r = vector(A[:,-_sage_const_1 ])
    A = A.change_ring(Zmod(m))[:,:_sage_const_2 ]

    try:
        a, b = A.solve_right(r)
    except ValueError:
        continue
    if not a.is_unit():
        continue

    assert a * x[_sage_const_0 ] + b == x[_sage_const_1 ]
    assert a * x[_sage_const_1 ] + b == x[_sage_const_2 ]
    assert a * x[_sage_const_2 ] + b == x[_sage_const_3 ]
    nxt = ZZ(a * x[_sage_const_3 ] + b)
    # if nxt & 0xff > 16 or not (nxt & 1):
    #     continue

    print('        a = \x1b[34m{}\x1b[0m'.format(hx(ZZ(a))))
    print('        b = \x1b[34m{}\x1b[0m'.format(hx(ZZ(b))))

    y = (x[_sage_const_0 ] - b) / a

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

