import struct

packets = [bytes.fromhex(line) for line in open('data.txt', 'r').read().splitlines()]

kb = [
    '_________________________1234567890-=\xff',
    '__0______________qwertyuiop{}\\__________',
    '_________asdfghjkl;\'_________',
    '__zxcvbnm,./',
    '_' * 32
]

flag = ''
for i in range(630, len(packets)-1, 2):
    rx = packets[i]
    tx = packets[i+1]
    if rx[0] != 0xa9 or tx[0] != 0xa9:
        continue

    if rx[1] != tx[1]:
        print(f'{i}: Packet has different commands rx={rx[1]:02x}, tx={tx[1]:02x}')
        continue

    command = rx[1]
    if command == 0x14:
        mode, act_pt, sens, rls_sens, entire, rm0, rm1, rm2, rm3, rm4 = struct.unpack('<BBBB?IIIII', rx[3:28])
        row_mask = [rm0, rm1, rm2, rm3, rm4]

        row = next(i for i, x in enumerate(row_mask) if x != 0)
        col = len(bin(row_mask[row])[2:]) - 1
        c = kb[row][col]
        print(row, col, c)
        flag += c
print(flag)
