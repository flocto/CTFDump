import capstone
import re
from binaryninja import *
from binaryninja.types import *

if not bv:
    bv = BinaryView()

main = bv.get_function_at(0x0001221)

# *(rax_4 + 0x2d810) = 0x997c9787
# *(THING + OFFSET) = VALUE
inst_format = r"\*\((.*?) \+ (0x[0-9a-f]+)\) = (0x[0-9a-f]+)"

offsets = []

for bb in main.hlil:
    for inst in bb:
        inst_str = f"{inst}"
        if (m := re.match(inst_format, inst_str)):
            offset, value = m.group(2), m.group(3)
            offset = int(offset, 16)
            value = int(value, 16)
            offsets.append((offset, value))

func2 = bv.get_function_at(0x001123e)
for bb in func2.hlil:
    for inst in bb:
        inst_str = f"{inst}"
        if (m := re.match(inst_format, inst_str)):
            offset, value = m.group(2), m.group(3)
            offset = int(offset, 16)
            value = int(value, 16)
            offsets.append((offset, value))

cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
tops = {}
ordered_tops = []

for offset, value in offsets:
    offset //= 8
    hi, lo = offset >> 8, offset & 0xff
    # print(hex(hi), hex(lo), hex(value))

    if hi not in tops:
        tops[hi] = []
        ordered_tops.append(hi)
    
    # try to disassemble the instruction
    insts = value.to_bytes(4, "little")
    try:
        insts = list(cs.disasm(insts, 0))
        # make sure last one is ret 
        if insts[-1].mnemonic != "ret" or len(insts) == 1:
            continue
        tops[hi].append((lo, insts))
    except:
        pass

for hi in ordered_tops:
    # print(hi, tops[hi])
    print(hi, [chr(x[0]) for x in tops[hi]])