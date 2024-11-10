import re
from z3 import *
# from cvc5.pythonic import *
set_param("parallel.enable", True)
import ctypes

parts = open('dump_reparsed.txt', 'r').read().split('cmovne')
op_dict = {
    'add': '+',
    'sub': '-',
    'xor': '^',
}


def split_part(part):
    out = []
    chunk = []
    for line in part.split('\n'):
        if line.startswith('==='):
            if chunk:
                out.append(chunk)
                chunk = []
            # out.append([line])
        else:
            chunk.append(line)
    if chunk:
        out.append(chunk)
    return out


def find_input_offset(chunk):
    shifts = re.findall(r'add rsp, [1-9][0-9]*', chunk)
    if shifts:
        return int(shifts[0].split(', ')[1])
    return 0


def find_add_const(chunk, next_chunk):
    shift = re.findall(r'shl .*, (.+)', next_chunk)
    if shift:
        # print(shift)
        shift = int(shift[0], 16)
    else:
        shift = 0
    add_const = re.findall(r'; UWOP_ALLOC_LARGE ([0-9]+)', chunk)
    # print(add_const)
    if add_const:
        return int(add_const[0]), shift
    return 0, shift


def find_sub_const(chunk, next_chunk):
    shift = re.findall(r'shl .*, (.+)', next_chunk)
    if shift:
        # print(shift)
        shift = int(shift[0], 16)
    else:
        shift = 0
    sub_const = re.findall(r'; UWOP_ALLOC_LARGE ([0-9]+)', chunk)
    # print(add_const)
    if sub_const:
        return int(sub_const[0]), shift
    return 0, shift


def find_xor_const(chunk, next_chunk):
    shift = re.findall(r'shl .*, (.+)', next_chunk)
    if shift:
        # print(shift)
        shift = int(shift[0], 16)
    else:
        shift = 0
    xor_offset = re.findall(r'add rsp, [1-9][0-9]*', chunk)
    # print(shifts)
    if xor_offset:
        return int(xor_offset[0].split(', ')[1]), shift
    return 0, shift


def find_or_const(chunk, next_chunk):
    shift = re.findall(r'shl .*, (.+)', next_chunk)
    if shift:
        # print(shift)
        shift = int(shift[0], 16)
    else:
        shift = 0
    or_offset = re.findall(r'add rsp, [1-9][0-9]*', chunk)
    # print(shifts)
    if or_offset:
        return int(or_offset[0].split(', ')[1]), shift
    return 0, shift


def find_mul_const(chunk):
    lines = chunk.split('\n')
    n = int(lines[1].split()[-1], 16)
    n += int(lines[2].split()[-1], 16)
    n &= 2**64 - 1
    return n


def find_inbetween_op(chunk):
    lines = chunk.split('\n')
    assert len(lines) == 2
    # print(lines)
    mnem = lines[1].split()[0]
    return op_dict[mnem]


def collapse(consts):
    n = 0
    for c in consts[::-1]:
        n <<= 8
        n += c
    return n

# s = Solver()
# flag = [BitVec(f'flag_{i}', 64) for i in range(0x20)]
# for f in flag:
#     s.add(f >= 32, f <= 126)


extracted = []
# flag = b"abcdefghijklmnopqrstuvwxyz123456789ABCDE"

for part in parts[:-1]:
    chunks = split_part(part)
    i = 0

    consts = []
    ops = []
    inputs = []
    inbetween = []
    while i < len(chunks):
        chunk = '\n'.join(chunks[i])

        if 'input' in chunk:
            # print(chunks[i+1])
            next_chunk = '\n'.join(chunks[i+1])
            offset = find_input_offset(next_chunk)
            # print(f'input offset: {offset}')
            inputs.append(offset)

        if 'mul' in chunk:
            # print(chunk)
            if len(inputs) > 1:
                next_chunk = '\n'.join(chunks[i+1])
                btwn = find_inbetween_op(next_chunk)
                inbetween.append(btwn)

            n = find_mul_const(chunk)
            consts.append(n)
            ops.append('mul')

        if '; add' in chunk:
            # print(chunk)
            next_chunk = '\n'.join(chunks[i+1])
            next_next_chunk = '\n'.join(chunks[i+2])
            n, shift = find_add_const(next_chunk, next_next_chunk)
            assert n % 8 == 0
            n //= 8
            # print('add', hex(n), shift)
            n = n << shift
            if ops[-1] != 'add':
                consts.append(n)
                ops.append('add')
                # print('add', hex(n), shift)
            else:
                # print('add', hex(n), shift, hex(consts[-1]))
                consts[-1] += n

        if '; sub' in chunk:
            # print(chunk)
            next_chunk = '\n'.join(chunks[i+1])
            next_next_chunk = '\n'.join(chunks[i+2])
            n, shift = find_sub_const(next_chunk, next_next_chunk)
            assert n % 8 == 0
            n //= 8
            # print('sub', hex(n), shift)
            n = n << shift

            if ops[-1] != 'sub':
                consts.append(n)
                ops.append('sub')
                # print('sub', hex(n), shift)
            else:
                # special case for sub
                if shift < consts[-1].bit_length():
                    consts.append(n)
                    ops.append('sub')
                    # print('sub', hex(n), shift)
                else:
                    # print('sub', hex(n), shift, hex(consts[-1]))
                    consts[-1] += n

        if '; xor' in chunk:
            next_chunk = '\n'.join(chunks[i+1])
            next_next_chunk = '\n'.join(chunks[i+2])
            n, shift = find_xor_const(next_chunk, next_next_chunk)
            assert n % 8 == 0
            n //= 8
            # print('xor', hex(n), shift)
            n = n << shift

            if ops[-1] != 'xor':
                consts.append(n)
                ops.append('xor')
                # print('xor', hex(n), shift)
            else:
                # print('xor', hex(n), shift, hex(consts[-1]))
                consts[-1] += n

        if '; or' in chunk:
            next_chunk = '\n'.join(chunks[i+1])
            next_next_chunk = '\n'.join(chunks[i+2])
            n, shift = find_or_const(next_chunk, next_next_chunk)
            assert n % 8 == 0
            n //= 8
            # print('or', hex(n), shift)
            n = n << shift

            # if ops[-1] != 'or':
            #     consts.append(n)
            #     ops.append('or')
            # else:
            #     consts[-1] += n

        i += 1

    # print(ops, consts, inputs, inbetween)

    last = ops[-1], consts[-1]
    eq = ''
    while inputs:
        inp = inputs.pop(0)
        op1, op2 = ops[:2]
        ops = ops[2:]
        c1, c2 = consts[:2]
        consts = consts[2:]
        assert op1 == 'mul'
        term = f"(flag[{inp}] * 0x{c1:x})"

        # term = f"(({flag[inp]} * {c1}) {op_dict[op2]} {c2})"
        if not eq:
            eq = term
        else:
            eq = f"({eq} {term})"
        eq = f'({eq} {op_dict[op2]} 0x{c2:x})'

        if inbetween:
            eq = f'{eq} {inbetween.pop(0)}'

    # eq = f'({eq}) {op_dict[last[0]]} {last[1]}'
    eq = f'({eq}) {op_dict[last[0]]} 0x{last[1]:x}'

    print(eq)
    extracted.append(eq)
    # extracted.append(ctypes.c_uint64(eval(eq)).value)

open('extracted.txt', 'w').write('\n'.join(extracted))  
# print(extracted)

# x = [18446744072095496842, 2026512031, 518287595, 5347206948, 18446744071942168121, 18446744069997896814, 18446744071707908866, 307525605, 18446744060885022799, 18446744072064824947, 524765812, 18446744068905596538, 18446744073434342216, 18446744073223182533, 1743441878, 18446744072816436052, 3902094250, 18446744073153217748, 1788660296, 18446744070803804988, 1505141882, 18446744073688758901, 18446744073192848747, 18446744067959049153, 725903655, 824365232, 18446744067590713081, 18446744072509864391, 18446744073586738091, 18446744072562476285, 18446744073291322558, 18446744065877534255] 

# for i, (e, y) in enumerate(zip(extracted, x)):
#     print(i, e == y)

s = Solver()
flag = [BitVec(f'flag_{i}', 64) for i in range(0x20)]
for f in flag:
    s.add(f >= 32, f <= 126)

a = [0, 1, 2, 3, 6, 10, 12, 20, 22, 28, 29, 30, 31]
# a = [2, 6, 10]
# a = list(range(0x20))


for i in a:
    s.add(eval(extracted[i]) == 0)

if s.check() == sat:
    m = s.model()
    print(i, ''.join([chr(m[f].as_long()) for f in flag]))
else:
    print(i, 'unsat')

# (((((((((((((((((((((((((flag[4] * 15694476))) + 0x9d865d8d) - (flag[24] * 4568380))) + 0x18baee57) - (flag[0] * 14995339))) - 0x913fbbde) - (flag[8] * 16107920))) + 0x6bfaa656) ^ (
#     flag[20] * 7549304))) ^ 0x61e3db3b) ^ (flag[16] * 10098616))) - 0xca2804b1) ^ (flag[12] * 7813200))) ^ 0x5a6f68be) ^ (flag[28] * 14818621))) ^ 0x5c911d23) - 0xffffffff81647a79

# ((((((((((((((((((flag[4] * 15694476)) + 0x9d865d8d) - (flag[24] * 4568380)) + 0x18baee57) - (flag[0] * 14995339)) - 0x913fbbde) - (flag[8] * 16107920)) + 0x6bfaa656) ^
#  (flag[20] * 7549304)) ^ 0x61e3db3b) ^ (flag[16] * 10098616)) - 0xca2804b1) ^ (flag[12] * 7813200)) ^ 0x5a6f68be) ^ (flag[28] * 14818621)) ^ 0x5c911d23)) - 0xffffffff81647a79

# (((((((((((((((((flag[4] * 15694476) + 0x9d865d8d) - (flag[24] * 4568380)) + 0x18baee57) - (flag[0] * 14995339)) - 0x913fbbde) - (flag[8] * 16107920)) + 0x6bfaa656) ^ (flag[20] * 7549304)) ^ 0x61e3db3b) ^ (flag[16] * 10098616)) - 0xca2804b1) ^ (flag[12] * 7813200)) ^ 0x5a6f68be) ^ (flag[28] * 14818621)) ^ 0x5c911d23)) - 0xffffffff81647a79