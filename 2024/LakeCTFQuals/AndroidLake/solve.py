import lief
import capstone
from z3 import *
import ctypes
import pickle

elf = lief.parse("libohgreat.so")
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
valid_funcs = open('valid.txt').read().split('\n')

flag = [BitVec(f'flag_{i}', 32) for i in range(63)]
s = Solver()
# for f in flag:
#     s.add(f >= 0x20, f <= 0x7e)

mapping = pickle.load(open('mapping.pkl', 'rb'))
valid_funcs = [mapping[f] for f in valid_funcs]

types = set()
rules = []
bodies = {}
for symbol in valid_funcs:
    symbol = elf.get_symbol(symbol)
    loc = elf.get_symbol(symbol.name).value

    byts = elf.get_content_from_virtual_address(loc, 0x100)

    disas = list(cs.disasm(byts, loc))
    # up until ret
    disas = disas[:disas.index(next(filter(lambda x: x.mnemonic == 'ret', disas)))+1]
    bodies[symbol.name] = disas
    # print(f"Symbol: {symbol.name}")
    idxs = []
    others = []
    res = 0
    for i in disas[5:]:
        # print(f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}")
        if i.mnemonic == "cmp":
            res = int(i.op_str.split(',')[1].strip(), 16)
            # unsigned 32 bit
            res &= 0xffffffff
            # res = ctypes.c_uint32(res).value
            continue
        if i.mnemonic == 'sete':
            print(f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}")
            break

        if i.mnemonic == 'movsx' or i.mnemonic == 'movzx':
            print(i.op_str)
            if '+' not in i.op_str:
                idxs.append(0)
                continue
            offset = int(i.op_str.split('+')[1][:-1].strip(), 16)
            idxs.append(offset)
        elif i.mnemonic == 'xor':
            if '+' not in i.op_str:
                idxs.append(0)
            else:
                offset = int(i.op_str.split('+')[1][:-1].strip(), 16)
                idxs.append(offset)
            others.append('xor')
        else:
            others.append(i.mnemonic)

    print(symbol.name)
    print([hex(i) for i in idxs], others, hex(res))
    assert len(idxs) == 3
    rules.append((*idxs, others, res))

    match others:
        case ['xor', 'xor']:
            s.add(flag[idxs[0]] ^ flag[idxs[1]] ^ flag[idxs[2]] == res)
        case ['add', 'add']:
            s.add(flag[idxs[0]] + flag[idxs[1]] + flag[idxs[2]] == res)
        case ['add', 'sub']:
            print(f'{flag[idxs[0]]} - ({flag[idxs[1]]} + {flag[idxs[2]]}) == {res}')
            s.add((flag[idxs[0]] + 0x1000) - (flag[idxs[1]] + flag[idxs[2]]) == res + 0x1000)
            # s.add(ZeroExt(24, flag[idxs[0]]) - (ZeroExt(24, flag[idxs[1]]) + ZeroExt(24, flag[idxs[2]])) == res)
            pass

with open('rules.txt', 'w') as f:
    for body in bodies:
        f.write(f"{body}\n")
        for i in bodies[body]:
            f.write(f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}\n")

if s.check() == sat:
    m = s.model()
    flag = ''.join([chr(m[f].as_long()) for f in flag]).encode()
    print(flag)
else:
    print('unsat')