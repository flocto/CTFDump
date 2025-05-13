import gdb

insts = []
for i in range(300):
    # rsi = gdb.parse_and_eval("$rsi")
    # inst = gdb.inferiors()[0].read_memory(rsi + 7, 8)
    # inst = int.from_bytes(inst, byteorder='little')
    # inst = gdb.parse_and_eval("$rax")
    # inst = int(inst)
    # insts.append(inst)

    rdi = gdb.parse_and_eval("$rdi")
    rsi = gdb.parse_and_eval("$rsi")
    rdx = gdb.parse_and_eval("$rdx")
    rcx = gdb.parse_and_eval("$rcx")
    rdi, rsi, rdx, rcx = int(rdi), int(rsi), int(rdx), int(rcx)
    insts.append(f'{rdi:x} {rsi} {rdx} {rcx}')
    gdb.execute("c")

# with open("insts.txt", "w") as f:
with open("insts2.txt", "w") as f:
    for i, inst in enumerate(insts):
        f.write(f'{i:04d}: {inst}\n')
# for i, inst in enumerate(insts):
#     print(f'{i:04d}: {inst}')