def shuffle(c):
    alpha = b'B2yO^?3[1$g5*,JKI4zsowp~HWT(9)ZUtLk\\7";rxb|RQnP]!G`mD+e\'>{Yhc/a0CN8q=}A<vSX&f@i_u6.-E#Vlj:%FdM'
    r3 = c - 33
    if r3 <= 93:
        return alpha[r3]
    return c

# uint8_t encode(unsigned char c, int idx)

#     uint32_t A
#     uint32_t A_1 = A
#     int32_t shuf_c = shuffle(x: c)
#     uint32_t B = 5
    
#     if (idx == idx s/ 5 * 5)
#         A = 2
#     else if (idx s% 5 - 1 u> 3)
#         B = 0
#     else
#         A = zx.d(ab[4][idx s% 5])
#         B = zx.d(ab[idx s% 5])
    
#     int32_t bit_A = 1 << A
#     int32_t bit_B = 1 << B
#     int32_t i = idx s% 11
#     uint32_t x = zx.d(((bit_A & shuf_c) u>> A << B).b) | ((bit_B & shuf_c) u>> B << A).b
#         | (shuf_c.b & (not.d(bit_A | bit_B)).b)
    
#     if (i == 0)
#         x -= 0x62
#         label_238:
        
#         if (x s< 0)
#             x += 0x100
#     else if (i - 1 u<= 9)
#         switch (i)
#             case 1
#                 x -= 2
#             case 2
#                 x -= 0x56
#             case 3
#                 x -= 0xf6
#             case 4
#                 x -= 0x46
#             case 5
#                 x -= 0xc
#             case 6
#                 x -= 0x99
#             case 7
#                 x -= 0x14
#             case 8
#                 x -= 0x85
#             case 9
#                 x -= 0xab
#             case 0xa
#                 x -= 0xba
        
#         goto label_238
    
#     return x.b

ab = b'\x00\x00\x01\x03\x02\x06\x03\x05\x04'
def encode(c, idx):
    shuf_c = shuffle(c)
    A = 0
    A_1 = A
    B = 5

    if idx % 5 == 0:
        A = 2
    elif idx % 5 - 1 > 3:
        B = 0
    else:
        A = ab[4 + (idx % 5)]
        B = ab[idx % 5]

    bit_A = 1 << A
    bit_B = 1 << B
    i = idx % 11
    x = ((bit_A & shuf_c) >> A << B) | ((bit_B & shuf_c) >> B << A) | (shuf_c & ~(bit_A | bit_B))

    if i == 0:
        x -= 0x62
        if x < 0:
            x += 0x100
    elif i - 1 <= 9:
        if i == 1:
            x -= 2
        elif i == 2:
            x -= 0x56
        elif i == 3:
            x -= 0xf6
        elif i == 4:
            x -= 0x46
        elif i == 5:
            x -= 0xc
        elif i == 6:
            x -= 0x99
        elif i == 7:
            x -= 0x14
        elif i == 8:
            x -= 0x85
        elif i == 9:
            x -= 0xab
        elif i == 0xa:
            x -= 0xba
        if x < 0:
            x += 0x100
    return x

enc = b'\xf4k\xf0\x17 K\xd2b\x9a\xb1\x8b\xd1w\xf1f\x1f)\xb4\x0b\xeb'
dec = ''
for i in range(0, len(enc)):
    for c in range(33, 127):
        if encode(c, i) == enc[i]:
            dec += chr(c)
            break

print(dec)
    