from z3 import *


N = 32
SIZE = 32 * 8
MASK = (1 << SIZE) - 1

first = BitVec('first', SIZE)
second = BitVec('second', SIZE)

sum_lower = b'k?!E\x06Q\x0e?l9\x883\x81\xb4\xb2>'
sum_upper = b'\xfe\xe3\xa1D:\xc6\x01:8\x01\xc5&\xf4\xdf\x971'

sum_lower = int.from_bytes(sum_lower, 'little')
sum_upper = int.from_bytes(sum_upper, 'little')

# VPMADDWD
first_words = [Extract(i * 16 + 15, i * 16, first) for i in range(16)]
second_words = [Extract(i * 16 + 15, i * 16, second) for i in range(16)]

dest = []
for i in range(8):
    a = ZeroExt(16, first_words[i * 2])
    b = ZeroExt(16, second_words[i * 2])
    left = a * b

    a = ZeroExt(16, first_words[i * 2 + 1])
    b = ZeroExt(16, second_words[i * 2 + 1])
    right = a * b

    dest.append(left + right)

dest = Concat(*dest[::-1])

dest_lower = Extract(127, 0, dest)
dest_upper = Extract(255, 128, dest)

s = Solver()
s.add(dest_lower == sum_lower)
s.add(dest_upper == sum_upper)

known_first =  b'stop_st0p_??????w3_n33d_t0_g0_B4'
known_second = b'ck...back_t0_R0cks_in_th3_d3sErt'
min_chr = b'!'[0]
max_chr = b'~'[0]

for i in range(32):
    first_byte = Extract(i * 8 + 7, i * 8, first)
    if known_first[i] != b'?'[0]:
        s.add(first_byte == known_first[i])
    else:
        s.add(UGE(first_byte, min_chr))
        s.add(ULE(first_byte, max_chr))
    
    second_byte = Extract(i * 8 + 7, i * 8, second)
    if known_second[i] != b'?'[0]:
        s.add(second_byte == known_second[i])
    else:
        s.add(UGE(second_byte, min_chr))
        s.add(ULE(second_byte, max_chr))

if s.check() == sat:
    m = s.model()
    while s.check() == sat:
        m = s.model()
        first_val = m[first].as_long()
        second_val = m[second].as_long()

        first_bytes = first_val.to_bytes(SIZE // 8, 'little')
        second_bytes = second_val.to_bytes(SIZE // 8, 'little')
        print(first_bytes + second_bytes)
        
        # Add constraint to avoid finding the same solution again
        s.add(Or(first != first_val, second != second_val))
else:
    print("No solution found")