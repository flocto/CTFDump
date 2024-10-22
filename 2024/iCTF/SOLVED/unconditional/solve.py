enc = 'b4,31,8e,02,af,1c,5d,23,98,7d,a3,1e,b0,3c,b3,c4,a6,06,58,28,19,7d,a3,c0,85,31,68,0a,bc,03,5d,3d,0b'
enc = [int(x, 16) for x in enc.split(',')]

table1 = b'RdqQTv'
table2 = b'\x01\x03\x04\x02\x06\x05'

counter1 = 0
counter2 = 0

# 0000128c      char flip = (table1[sx.q(iterate(int32_t)::counter1)] ^ (C u>> 2 | C << 6)) * (not_alpha ^ 1) + not_alpha * ((zx.d(C) << (8 - table2[sx.q(iterate(int32_t)::counter2)])).b | (zx.d(C) s>> table2[sx.q(iterate(int32_t)::counter2)]).b)
# 000012a3      (*"nothing_here_lmao")[sx.q(i)] = odd * ((C u>> 6 | C << 2) * (not_alpha ^ 1) + not_alpha * (table1[sx.q(iterate(int32_t)::counter1)] ^ C)) + (odd ^ 1) * flip

for i, e in enumerate(enc):
    is_odd = i % 2

    if is_odd:
        alpha = (e >> 2) | (e << 6)
        not_alpha = e ^ table1[counter1]
    else:
        alpha = e ^ table1[counter1]
        alpha = (alpha >> 6) | (alpha << 2)
        not_alpha = (e >> (8 - table2[counter2])) | (e << table2[counter2])

    alpha = alpha & 0xff
    not_alpha = not_alpha & 0xff

    if alpha in range(ord('a'), ord('z') + 1):
        print(chr(alpha), end='')
    else:
        print(chr(not_alpha), end='')

    # print(bytes([alpha, not_alpha]))
    counter1 = (counter1 + is_odd) % 6
    counter2 = (counter2 + is_odd) % 6