D = 2654435769

key_idxs = [3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 0, 0, 2, 2, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1]

blocks = [key_idxs[i:i+32] for i in range(0, len(key_idxs), 32)]

dec_key_idxs = sum(blocks[::-1], [])

def enc(dat, key):
    global D
    s = 0
    for X in range(5):
        s += D
        for i in range(len(dat)):
            a, c = dat[i-1], dat[(i+1) % len(dat)]
            k = (((a >> 3) ^ (c << 3)) + ((c >> 4) ^ (a << 2))) & 0xFFFFFFFF
            # print(i, k)

            idx = key_idxs[X*32 + i]
            # print(i, idx, key[idx])

            d = ((c ^ s) + (key[idx] ^ a)) & 0xFFFFFFFF
            dat[i] += (k ^ d) & 0xFFFFFFFF
            dat[i] &= 0xFFFFFFFF
            # print(i, dat[i])

    return dat

def dec(dat, key):
    global D
    s = D * 5
    N = 5
    for X in range(N):
        for i in range(len(dat)-1, -1, -1):
            a, c = dat[i-1], dat[(i+1) % len(dat)]
            k = (((a >> 3) ^ (c << 3)) + ((c >> 4) ^ (a << 2))) & 0xFFFFFFFF

            idx = dec_key_idxs[X*32 + i]
            # print(i, idx, key[idx])

            d = ((c ^ s) + (key[idx] ^ a)) & 0xFFFFFFFF
            dat[i] -= (k ^ d) & 0xFFFFFFFF
            dat[i] &= 0xFFFFFFFF

        s -= D

    return dat

key = b'SyC1'
# test = b'SCTF{abcd1234ABCD5678efgh1234AA}'

# dat = [x for x in test]
# key = [x for x in key]

# dat = enc(dat, key)

# print(dat)

dat = [4108944556, 3404732701, 1466956825, 788072761, 1482427973, 782926647, 1635740553, 4115935911, 2820454423, 3206473923, 1700989382, 2460803532, 2399057278, 968884411, 1298467094, 1786305447, 3953508515, 2466099443, 4105559714, 779131097, 288224004, 3322844775, 4122289132, 2089726849, 656452727, 3096682206, 2217255962, 680183044, 3394288893, 697481839, 1109578150, 2272036063]

dat = dec(dat, key)

print(bytes(dat))