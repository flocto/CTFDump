import lief
import capstone


elf = lief.parse("libohgreat.so")
cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
sym = elf.get_symbol('JNI_OnLoad')
print(sym, sym.size)
dat = open('libohgreat.so', 'rb').read()

insts = elf.get_content_from_virtual_address(sym.value, sym.size)
insts = list(cs.disasm(insts, sym.value))
valid_funcs = open('valid.txt').read().split('\n')
addrs = open('lol.txt').read().split('\n')

def get_func_at(eaddr):
    for line in addrs:
        addr, func = line.split('  ', 1)
        if int(addr, 16) == eaddr:
            return func.strip().split(' ')[-1]

mapping = {

}
for i in insts:
    if i.mnemonic == 'mov':
        if 'rip' in i.op_str:
            print(f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}")
            addr = int(i.op_str.split('+')[1][:-1], 16) + i.address + i.size
            print(hex(addr))
            symbol = get_func_at(addr)
            print(symbol)
            mapping[valid_funcs[len(mapping)]] = symbol

import pickle
pickle.dump(mapping, open('mapping.pkl', 'wb'))