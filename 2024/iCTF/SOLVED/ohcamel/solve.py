import lief
import struct

elf = lief.parse("main.exe")

grid = []

for i in range(1, 66):
    sym_name = f'camlDune__exe__Main__{i}'
    sym = elf.get_symbol(sym_name)
    addr = sym.value
    
    # 65 long longs
    data = elf.get_content_from_virtual_address(addr, 65 * 8)
    data = struct.unpack("Q" * 65, data)
    data = [x // 2 for x in data]
    data = ['.' if x == 1 else '#' for x in data]
    grid.append(data)

for row in grid:
    print(''.join(row))

visited = set()
s = (0, 0)
e = (64, 64)
visited.add(s)
q = [(s, '')]

while q:
    (x, y), path = q.pop(0)
    if (x, y) == e:
        print(path)
        break

    for d, (dx, dy) in enumerate([(0, 1), (0, -1), (1, 0), (-1, 0)]):
        nx, ny = x + dx, y + dy
        if 0 <= nx < 65 and 0 <= ny < 65 and grid[nx][ny] == '.' and (nx, ny) not in visited:
            visited.add((nx, ny))
            q.append(((nx, ny), path + 'RLDU'[d]))

empty_grid = grid.copy()
s = (0, 0)
empty_grid[s[0]][s[1]] = 'S'
for p in path:
    dx, dy = [(0, 1), (0, -1), (1, 0), (-1, 0)]['RLDU'.index(p)]
    s = (s[0] + dx, s[1] + dy)
    empty_grid[s[0]][s[1]] = 'X'

for row in empty_grid:
    print(''.join(row))