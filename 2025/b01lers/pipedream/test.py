data = open('pipe-dream', 'rb').read()

grid = data[0x3020:0x3020 + 70]
grid = [grid[i:i+10] for i in range(0, len(grid), 10)]

# LDRU
cells = ' ╵╶└╷│┌├╴┘─┴┐┤┬┼'

rotations = [
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    [0, 0, 2, 0, 0, 2, 0, 0, 0, 0],
    [1, 0, 3, 3, 0, 1, 1, 1, 2, 1],
    [3, 1, 3, 1, 3, 3, 1, 2, 1, 1],
    [1, 1, 3, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 2, 0, 0],
    [0, 1, 1, 2, 0, 0, 2, 0, 0, 0],
]


out_grid = []
for i, row in enumerate(grid):
    out_row = []
    for j, cell in enumerate(row):
        rotation = rotations[i][j]
        cell = ((cell << rotation) | (cell >> (4 - rotation))) & 0xF
        out_row.append(cells[cell])
    out_grid.append(out_row)

for row in out_grid:
    print(''.join(row))

print(''.join(''.join(map(str, row)) for row in rotations))