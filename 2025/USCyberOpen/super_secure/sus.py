import gdb

start = 0x5555555551e0
length = 0x20000

mem = gdb.inferiors()[0].read_memory(start, length)
with open('dump.bin', 'wb') as f:
    f.write(mem)