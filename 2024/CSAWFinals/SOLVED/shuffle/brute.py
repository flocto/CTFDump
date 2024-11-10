from pwn import elf, process, remote
import random

elf = elf.ELF('./shuffle')

grid = [
    15, 1, 2, 3,
    4, 7, 5, 6,
    8, 10, 12, 11,
    9, 13, 14, 0
] # 93
# grid = [
#     15, 12, 3, 2,
#     4, 8, 5, 6,
#     10, 7, 9, 11,
#     1, 13, 14, 0
# ]

# random.shuffle(grid)
# grid = ' '.join(map(str, grid))
# print(grid)

grid = "4 6 15 14 1 7 2 5 10 11 12 0 8 13 9 3"

i = 0
impossible = set()
while True:
    i += 1
    if i % 100 == 0:
        print(i)
    # r = process('./shuffle', level='error')
    # chals.ctf.csaw.io:30017
    r = remote('chals.ctf.csaw.io', 30017, level='error')
    # r = remote('chals.ctf.csaw.io', 30017, level='debug')
    r.sendlineafter(b'y/n: ', b'\x00')
    r.recvline() # remote only
    line = r.recvline().strip()
    if b'Please' in line:
        r.close()
        continue
    print(line)

    # r_grid = grid.copy()
    # random.shuffle(r_grid)
    # while tuple(r_grid) in impossible:
    #     random.shuffle(r_grid)

    # r_grid_str = ' '.join(map(str, r_grid))
    # print(r_grid_str)
    # r.interactive()

    r.sendline( grid.encode())
    # r.sendlineafter(b'grid!\n', grid.encode())
    r.recvline()

    r.sendline(b'cat flag.txt')
    print(r.recvall(10))
    break   
    # if b'not possible' in r.recvline():
    #     print('not possible')
    #     impossible.add(tuple(r_grid))
    #     r.close()
    #     continue
    # moves = r.recvline_contains(b'Moves: ')
    # print(moves)
    # if b'100' in moves:
    #     print('HOLLLYYYY FUCKKKK', r_grid)
    #     r.close()
    #     continue
    # # r.close()
    # r.interactive()
    # break