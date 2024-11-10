import re
from z3 import *

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

def find_add_const(chunk):
    add_carry = re.findall(r'add_carry\n(.*)\n', chunk)
    if add_carry:
        inner = re.findall(r'\[(.*)\]', add_carry[0])[0].split(' + ')
        if len(inner) == 2:
            return int(inner[1], 16)
    return 0

def find_sub_const(chunk):
    sub_carry = re.findall(r'sub_carry\n(.*)\n', chunk)
    if sub_carry:
        inner = re.findall(r'\[(.*)\]', sub_carry[0])[0].split(' + ')
        if len(inner) == 2:
            return int(inner[1], 16)
    return 0

def find_xor_const(chunk):
    shifts = re.findall(r'add rsp, [1-9][0-9]*', chunk)
    # print(shifts)
    if shifts:
        return int(shifts[0].split(', ')[1])
    return 0

def find_mul_const(chunk):
    lines = chunk.split('\n')
    n = int(lines[1].split()[-1], 16)
    n += int(lines[2].split()[-1], 16)
    n &= 2**64 - 1
    return n

def find_inbetween_op(chunk):
    lines = chunk.split('\n')
    assert len(lines) == 2
    mnem = lines[1].split()[0]
    return op_dict[mnem]

def collapse(consts):
    n = 0
    for c in consts[::-1]:
        n <<= 8
        n += c
    return n

s = Solver()
flag = [BitVec(f'flag_{i}', 56) for i in range(0x20)]
for f in flag:
    s.add(f >= 32, f <= 126)

extracted = []

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
        
        if 'add_carry' in chunk:
            # print(chunk)
            n = find_add_const(chunk)
            assert n % 8 == 0
            consts.append(n // 8)
            # print(consts)
            ops.append('add')

        if 'sub_carry' in chunk:
            # print(chunk)
            n = find_sub_const(chunk)
            assert n % 8 == 0
            consts.append(n // 8)
            # print(consts)
            ops.append('sub')

        if '; xor' in chunk:
            next_chunk = '\n'.join(chunks[i+1])
            n = find_xor_const(next_chunk)
            assert n % 8 == 0
            n //= 8
            consts.append(n)
            # print(consts)
            ops.append('xor')
        
        # if '; or' in chunk:
        #     print(chunk)

        i += 1

    # print(ops)
    # print(consts)

    # DO NOT CODE LIKE THIS EVER AGAIN 
    print(consts[-1])
    possible_lasts = [consts[-i:] for i in range(4, 8)]
    print(possible_lasts)

    if consts[-1] == 255:
        last = possible_lasts[-1]
        ops = ops[:-7]
    else:
        # get the last one whose first element is not 0
        for i in range(3):
            if possible_lasts[i][0] != 0 and possible_lasts[i+1][0] == 0:
                last = possible_lasts[i]
                ops = ops[:-i-4]
                break
        else:
            last = possible_lasts[-1]
            ops = ops[:-7]

    last = ('sub', hex(collapse(last)))
    cur_op = ops[0]
    i = 0
    eqs = []
    while i < len(ops):
        while i < len(ops) and ops[i] == cur_op:
            i += 1
        eqs.append((cur_op, hex(collapse(consts[:i]))))
        consts = consts[i:]
        ops = ops[i:]
        if ops:
            cur_op = ops[0]
        i = 0

    # print(inputs, len(inputs))
    # print(eqs, len(eqs))
    # print(inbetween, len(inbetween))

    # print(last[0], last[1])
    assert last[0] == 'sub'

    eq = ''
    while inputs:
        term = ''
        inp = inputs.pop(0)

        eq1 = eqs.pop(0)
        assert eq1[0] == 'mul'
        term = f'(flag[{inp}] * {eq1[1]})'

        if eq:
            eq = f'({eq} {term})'
        else:
            eq = term

        eq2 = eqs.pop(0)
        op = op_dict[eq2[0]]
        eq = f'({eq} {op} {eq2[1]})'

        if inputs:
            eq += f' {inbetween.pop(0)} '

    eq += f' {op_dict[last[0]]} {last[1]}'
    print(eq)
    extracted.append(eq)

# for eq in extracted[:1]:
#     s.add(eval(eq) == 0)

s.add(eval(extracted[0]) == 0)

if s.check() == sat:
    m = s.model()
    print(''.join([chr(m[f].as_long()) for f in flag]))
else:
    print('unsat')