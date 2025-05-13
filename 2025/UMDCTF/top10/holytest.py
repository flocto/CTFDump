def mpsadbw(source1, source2, imm8=0):
    result = []

    # source1 = int.from_bytes(source1, 'little')
    # source2 = int.from_bytes(source2, 'little')

    print(source1)
    print(source2)

    BLK2_OFFSET = (imm8 & 0x3) * 4
    BLK1_OFFSET = ((imm8 >> 2) & 0x1) * 4

    print(f'BLK2_OFFSET: {BLK2_OFFSET}')
    print(f'BLK1_OFFSET: {BLK1_OFFSET}')

    print(source1[BLK1_OFFSET:])
    print(source2[BLK2_OFFSET:])

    # low bytes
    for i in range(8):
        s = 0
        for j in range(4):
            src1_byte = source1[i + j + BLK1_OFFSET]
            src2_byte = source2[j + BLK2_OFFSET]

            s += abs(src1_byte - src2_byte)
        result.append(s)
    
    # BLK2_OFFSET = ((imm8 >> 3) & 0x3) * 4
    # BLK1_OFFSET = ((imm8 >> 5) & 0x1) * 4
    # # high bytes
    # for i in range(8):
    #     s = 0
    #     for j in range(4):
    #         src1_byte = source1[i + j + 16 + BLK1_OFFSET]
    #         src2_byte = source2[j + 16 + BLK2_OFFSET]

    #         s += abs(src1_byte - src2_byte)
    #     result.append(s)

    return result
    
K = 0x1337c0dedeadbeef
K = K.to_bytes(32, 'little')
print(K)

# inp = 0x3232323243434343313131316262626230303030414141416767676746464646
# inp = inp.to_bytes(32, 'little')
inp_bytes = b'fQ2A1HevnExPPPPPPPPPPPPPPPPPPPPP'
inp_bytes = b'aaaabbbbccccdddd5555666677778888'
print(inp_bytes)

res = mpsadbw(inp_bytes, K, 0)
# res = mpsadbw(K, inp_bytes)
res = [hex(x) for x in res]
print(res)

res = mpsadbw(inp_bytes, K, 5)
# res = mpsadbw(K, inp_bytes, 5)
res = [hex(x) for x in res]
print(res)
