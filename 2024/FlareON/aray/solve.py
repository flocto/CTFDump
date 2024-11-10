import z3
import hashlib
import zlib


rule = open('aray.yara', 'r').read().strip().split('\n')[7]

rules = [x.strip() for x in rule.split('and') if x][2:]

filesize = 85
flag = [z3.BitVec('flag_%d' % i, 8) for i in range(filesize)]
s = z3.Solver()

for f in flag:
    s.add(f >= 0x20)
    s.add(f <= 0x7e)

def uint8(x):
    return flag[x]

def uint32(x): # little endian
    return z3.Concat(flag[x + 3], flag[x + 2], flag[x + 1], flag[x])

def brute(hsh, x):
    for i in range(0x20, 0x7f):
        for j in range(0x20, 0x7f):
            if hsh(bytes([i, j])).hexdigest() == x:
                return i, j

for rule in rules:
    if '%' in rule:
        continue
    if '<' in rule:
        # print('Failed to parse rule:', rule)
        continue

    try:
        expr = eval(rule)
        s.add(expr)
        # print(rule, '=>', expr)
    except:
        # print('Failed to parse rule:', rule)    
        # pass
        hsh, rst = rule.split('(')
        hsh = hsh.split('.')[-1]
        
        idx = int(rst.split(',')[0])
        x = rst.split(' == ')[-1]
        # print(hsh, idx, x)

        if hsh == 'crc32':
            for i in range(0x20, 0x7e):
                for j in range(0x20, 0x7e):
                    if zlib.crc32(bytes([i, j])) & 0xffffffff == int(x, 16):
                        # print(bytes([i, j]), x)
                        s.add(flag[idx] == i)
                        s.add(flag[idx + 1] == j)
                        break
        elif hsh == 'md5':
            i, j = brute(hashlib.md5, x[1:-1])
            s.add(flag[idx] == i)
            s.add(flag[idx + 1] == j)
        elif hsh == 'sha256':
            i, j = brute(hashlib.sha256, x[1:-1])
            s.add(flag[idx] == i)
            s.add(flag[idx + 1] == j)


if s.check() == z3.sat:
    m = s.model()
    # print(m)
    print(''.join([chr(m[flag[i]].as_long()) for i in range(filesize)]))
else:
    print('Failed to solve')