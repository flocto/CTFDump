import json
from collections import namedtuple

# Define BitFields to hold decoded components
BitFields = namedtuple("BitFields", ["rhsMode", "rhsVal", "signBit", "lhsMode", "lhsVal"])

# Function to decode number into bit fields
def decode_number(number):
    rhsMode = number & 3
    rhsVal = (number >> 2) & 0xFF
    signBit = (number >> 10) & 1
    lhsMode = (number >> 11) & 3
    lhsVal = (number >> 13) & 0xFF
    return BitFields(rhsMode, rhsVal, signBit, lhsMode, lhsVal)


# Define the opcode mapping based on the Java code
OPCODE_MAP = {
    1: "mov",
    2: "xor",
    3: "ror",
    4: "cmp",
    6: "jne",
    7: "jmp",
    8: "call",
    9: "loop",
    10: "push",
    11: "pop",
    12: "repe",
    13: "dec",
    14: "inc",
    16: "ret",
    17: "syscall",
    # Opcodes 5 and 15 are marked as unimplemented
}

# Disassembler function
def disassemble(instruction_list, bufs):
    disassembly = []
    for addr, instruction in enumerate(instruction_list):
        # Unpack the instruction elements
        ops, opm, lhs, rhs = instruction

        # Get the mnemonic or mark as unimplemented
        if ops in OPCODE_MAP:
            mnemonic = OPCODE_MAP[ops]
            if ops == 1:  # Detailed "mov" handling based on opm
                if opm == 1:
                    disassembly.append((addr, f"mov r{lhs}, r{rhs}"))
                elif opm == 2:
                    disassembly.append((addr, f"mov r{lhs}, 0x{rhs:x}"))
                elif opm == 3:
                    disassembly.append((addr, f"mov r{lhs}, {bytes(bufs[str(rhs)])}"))
                elif opm == 4:
                    # Decode rhs into components and construct instruction description
                    fields = decode_number(rhs)
                    disassembly.append((addr, f"mov r{lhs}, decoded_value(rhsMode={fields.rhsMode}, rhsVal={fields.rhsVal}, "
                                       f"signBit={fields.signBit}, lhsMode={fields.lhsMode}, lhsVal={fields.lhsVal})"))
                elif opm == 5:
                    # Decode lhs into components and construct memory operation
                    fields = decode_number(lhs)
                    disassembly.append((addr, f"mov mem(decoded_lhs=({fields}), rhs={rhs})"))
                elif opm == 6:
                    # Decode lhs into components and include rhs as part of address size
                    fields = decode_number(lhs)
                    disassembly.append((addr, f"mov mem(decoded_lhs=({fields}), reg{rhs}, rhs_val={rhs})"))
                else:
                    raise Exception(f"Unimplemented mov operation for opm={opm}")
            elif ops == 2:  # "xor" instruction with detailed `opm` handling
                if opm == 1:
                    # Decode lhs and interpret as fields for memory operations
                    fields = decode_number(lhs)
                    disassembly.append((addr, f"xor mem(decoded_lhs=({fields}), reg{rhs}, rhsSize={8 if fields.rhsVal != 18 else 1})"))
                elif opm == 2:
                    disassembly.append((addr, f"xor r{lhs}, r{rhs}"))
                elif opm == 3:
                    fields = decode_number(rhs)
                    disassembly.append((addr, f"xor r{lhs}, decoded_rhs(fields={fields})"))
                else:
                    raise Exception(f"Unimplemented xor operation for opm={opm}")
            elif ops == 3:  # "ror" instruction with detailed `opm` handling
                if opm == 1:
                    disassembly.append((addr, f"ror r{lhs}, r{rhs}"))
                elif opm == 2:
                    fields = decode_number(lhs)
            #         BitFields m2076decodeNumberVKZWuLQ = m2076decodeNumberVKZWuLQ(lhs);
            # long rhsMode = m2076decodeNumberVKZWuLQ.m2100component1sVKNKU();
            # long rhsVal = m2076decodeNumberVKZWuLQ.m2101component2sVKNKU();
            # long signBit = m2076decodeNumberVKZWuLQ.m2102component3sVKNKU();
            # long lhsMode = m2076decodeNumberVKZWuLQ.m2103component4sVKNKU();
            # long lhsVal = m2076decodeNumberVKZWuLQ.m2104component5sVKNKU();
            # if (lhsMode == 1) {
            #     j = m2078readFromRegPUiSbYQ(lhsVal);
            # } else if (lhsMode == 2) {
            #     Integer num = this.mappings.get(Integer.valueOf((int) lhsVal));
            #     Intrinsics.checkNotNull(num);
            #     j = ULong.m515constructorimpl(num.intValue());
            # } else {
            #     j = lhsVal;
            # }
            # long lhsSum = j;
            # if (rhsMode == 1) {
            #     j2 = m2078readFromRegPUiSbYQ(rhsVal);
            # } else if (rhsMode == 2) {
            #     Integer num2 = this.mappings.get(Integer.valueOf((int) rhsVal));
            #     Intrinsics.checkNotNull(num2);
            #     j2 = ULong.m515constructorimpl(num2.intValue());
            # } else {
            #     j2 = rhsVal;
            # }
            # long rhsSum = j2;
            # long lhsFinal = signBit == 0 ? ULong.m515constructorimpl(lhsSum + rhsSum) : ULong.m515constructorimpl(lhsSum - rhsSum);
            # m2079writeToMemtwO9MuI(lhsFi
                    if fields.lhsMode == 1:
                        j = f"r{fields.lhsVal}"
                    elif fields.lhsMode == 2:
                        j = f"[{fields.lhsVal}]"
                    else:
                        j = f"{fields.lhsVal}"
                    lhsSum = j
                    if fields.rhsMode == 1:
                        j2 = f"r{fields.rhsVal}"
                    elif fields.rhsMode == 2:
                        j2 = f"[{fields.rhsVal}]"
                    else:
                        j2 = f"{fields.rhsVal}"
                    rhsSum = j2
                    lhsFinal = f"{lhsSum} + {rhsSum}" if fields.signBit == 0 else f"{lhsSum} - {rhsSum}"
                    disassembly.append((addr, f"ror [{lhsFinal}], {rhs}"))

            elif ops == 13: # dec
                disassembly.append((addr, f"dec r{lhs}"))
            elif ops == 14: # inc
                disassembly.append((addr, f"inc r{lhs}"))
            elif ops == 10: # push
                disassembly.append((addr, f"push r{lhs}"))
            elif ops == 11: # pop
                disassembly.append((addr, f"pop r{lhs}"))
            elif ops in {7, 8}:  # call, jmp
                disassembly.append((addr, f"call {lhs}"))
            elif ops in {5, 15}:
                raise Exception(f"Opcode {ops} is unimplemented.")
            elif ops in {3, 4}:  # Instructions with opm, lhs, rhs
                disassembly.append((addr, f"{mnemonic} opm={opm}, lhs={lhs}, rhs={rhs}"))
            elif ops in {6, 7, 8, 9, 10, 11}:  # Instructions with lhs
                disassembly.append((addr, f"{mnemonic} lhs={lhs}"))
            else:  # Instructions without operands, like "ret", "syscall", etc.
                disassembly.append((addr, mnemonic))
        else:
            raise Exception(f"Unknown opcode {ops}")

    return "\n".join(f"{addr:3}: {instr}" for addr, instr in disassembly)

program = json.loads(open('program.json').read())
code = program['code']
bufs = program['buf']

for b in bufs:
    bufs[b] = bytes(bufs[b])
    print(b, bufs[b])
# print(code, bufs)

code = [code[i:i+4] for i in range(0, len(code), 4)]

print(disassemble(code, bufs))