# from pwn import remote
from tqdm import trange
# nc 34.42.147.172 8009
# r = remote('34.42.147.172', 8009)

# infos = []
# for _ in trange(500):
#     r.sendlineafter(b'> ', b'2')
#     info = r.recvline_contains(b'Additional Info: ').strip().split(b' ')[-1]
#     infos.append(int(info))

# infos = sorted(set(infos))
# print(len(infos), infos)
infos = [
    275594854318,   # .
    306875722638,   # /
    340934651794,   # 0
    461629137298, 
    878091473854, 
    1129884591208, 
    1327634768734,  # ?
    1675263512638, 
    1806065932258, 
    4958875511998, 
    6292119317358, 
    11485295168188, 
    12089607308094, 
    12719093260930, 
    14056716232848, 
    14766457937518, 
    15504583147174, 
    16271934798450, 
    19651046343154, 
    20577758288920, 
    22536054359758, 
    23569580114578, 
    25750374470590, 
    26899692041938, 
    28089686233938, 
    29321427339808, # u
    30596004264814, # v
    31914524686710, # w
    34687921557268, # y
    37650860919994, # {
    40812896371368  # }
]

print(len(infos), infos)

for i in range(len(infos) - 1):
    print(i, infos[i], infos[i+1], infos[i+1] - infos[i], (infos[i+1] - infos[i]) / (3e10))

coords = [
    (b'}'[0], infos[-1]),
    (b'{'[0], infos[-2]),
    (b'y'[0], infos[-3]),
    # (b'w'[0], infos[-4]),
    # (b'v'[0], infos[-5]),
    # (b'u'[0], infos[-6]),
    # (b't'[0], infos[-7]),
    # (b'?'[0], infos[6]),
    
    (b'.'[0], infos[0]),
    (b'/'[0], infos[1]),
    (b'0'[0], infos[2]),
]

from sympy import Matrix
from numpy import poly1d

mat = []
vec = []
for x, y in coords:
    vec.append(y)   
    row = []
    for i in range(len(coords)):
        row.append(x ** i)
    mat.append(row)

mat = Matrix(mat)
vec = Matrix(vec)
coeff = mat.inv() @ vec

poly = poly1d(list(coeff.T)[::-1])
print(poly)

close = {}
alphas = []
for x in range(32, 127):
    y = poly(x)
    if y in infos:
        close[y] = chr(x)
        alphas.append(chr(x))

print(''.join(alphas))
