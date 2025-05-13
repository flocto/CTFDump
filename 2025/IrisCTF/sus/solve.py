import struct
from math import floor, sqrt
from lightsout import LightsOut

bmp = open('b3b6db05f1888b1603560e78a9564d9c.bmp', 'rb').read()

def get_4wide_at(bmp, idx):
    return struct.unpack('<I', bmp[idx:idx+4])[0]

offset = get_4wide_at(bmp, 0x0A)
width = get_4wide_at(bmp, 0x12)
height = get_4wide_at(bmp, 0x16)

def get_bmppixel(x, y):
    return get_4wide_at(bmp, offset + (height - y - 1) * width * 4 + x * 4)

def weird(k):
    # iVar2 = (int)FLOOR((SQRT((double)k * 8.0 + 1.0) + -1.0) * 0.5);
    ivar2 = floor((sqrt(k * 8.0 + 1.0) - 1.0) * 0.5)
    ivar1 = k - (ivar2 * (ivar2 + 1) >> 1)
    k = ivar2 - ivar1
    return k, (k | ivar1 * 0x100) >> 8

alpha = 'abcdefghijklmnopqrstuvwxyz0123456789'
lookup = {}
for i in range(36):
    # print(i, weird(i))
    k, inv_k = weird(i)
    lookup[(k, inv_k)] = i

lo = LightsOut(6)
for n in range(5):
    pix = get_bmppixel(0, n)
    x = (pix >> 8) & 0xFF
    y = pix & 0xFF

    # print(x, y)

    a_grid = []
    b_grid = []
    for i in range(6):
        a_row = []
        b_row = []
        for j in range(6):
            # row.append((get_bmppixel(x + j, y + i) & 0x100, get_bmppixel(x + j + 6, y + i) & 0x100 ))
            # row.append((hex(get_bmppixel(x + j, y + i)), hex(get_bmppixel(x + j + 6, y + i))))
            a_row.append((get_bmppixel(x + j, y + i) & 0x100) >> 8)
            b_row.append((get_bmppixel(x + j + 6, y + i) & 0x100) >> 8)
        a_grid.append(a_row)
        b_grid.append(b_row)

    # for row in a_grid:
    #     print(''.join(map(str, row)).replace('0', '.').replace('1', '#'), end='\n')
    # print()
    # for row in b_grid:
    #     print(''.join(map(str, row)).replace('0', '.') .replace('1', '#'), end='\n')

    a_sol = lo.solve(a_grid).flatten()
    b_sol = lo.solve(b_grid).flatten()

    out = ''
    for i in range(0, 36, 3):
        k = (a_sol[i + 2] << 2) | (a_sol[i + 1] << 1) | a_sol[i]
        inv_k = (b_sol[i + 2] << 2) | (b_sol[i + 1] << 1) | b_sol[i]
        out += alpha[lookup[(k, inv_k)]]

    print(out)

