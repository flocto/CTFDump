import re

insts = open('dump_lifted.txt', 'r').read().split('\n')

pairs = {}
potential_pairs = set()

addr_map = {
    0x14089b8e8: 'input',
    0x140095ac0: 'add',
    0x1400962c0: 'add_carry',
    0x140096ac0: 'sub',
    0x1400972c0: 'sub_carry',
    0x140094ac0: 'xor',
    0x1400952c0: 'or',
}

for i, inst in enumerate(insts):
    consts = re.findall(r'0x[0-9a-f]+', inst)

    to_del = set()
    for c in consts:
        for p_i, p in potential_pairs:
            if int(c, 16) + p in addr_map:
                pairs[(p_i, i)] = (p, int(c, 16))
                potential_pairs.remove((p_i, p))
                break
            elif i > p_i + 0x100:
                # potential_pairs.remove((p_i, p))
                to_del.add((p_i, p))
        else:
            potential_pairs.add((i, int(c, 16)))

    for p in to_del:
        potential_pairs.remove(p)

    if 'cmovne' in inst:
        print(f'{i}: {inst}')
    elif 'HLT' in inst:
        insts[i] = '=== ' + inst.split()[1]
    # elif ';' in inst:
    #     insts[i] = ''


for k, v in pairs.items():
    # print(f'{k[0]}: {insts[k[0]]}, {k[1]}: {insts[k[1]]} -> 0x{v[0] + v[1]:x}')
    insts[k[1]] += f'; {addr_map[v[0] + v[1]]}'

insts = [i for i in insts if i]
open('dump_reparsed.txt', 'w').write('\n'.join(insts))