from z3 import *

charset = list(b'chalkiest')

across_hints = [
    b'each',
    b'takeshi',
    b'castle',
    b'is',
    b'ethical',
    b'hacks',
]

down_hints = [
    b'chalkiest',
    b'lake',
]

# solve 9x9 "sudoku" board with given charset such that all the hints appear at least once, across horizonally and down vertically

board = [[BitVec(f'cell_{i}_{j}', 8) for j in range(9)] for i in range(9)]
def is_valid_cell(cell):
    return Or(
        *[cell == c for c in charset]
    )

s = Solver()
# all in charset
for i in range(9):
    for j in range(9):
        s.add(is_valid_cell(board[i][j]))
    
# sudoku row constraints
for i in range(9):
    s.add(Distinct(board[i]))

# sudoku column constraints
for j in range(9):
    s.add(Distinct([board[i][j] for i in range(9)]))

# sudoku box constraints
for box_i in range(3):
    for box_j in range(3):
        s.add(Distinct([board[i][j] for i in range(box_i * 3, (box_i + 1) * 3) for j in range(box_j * 3, (box_j + 1) * 3)]))

# add across hints
for hint in across_hints:
    hint_locations = []
    for i in range(9):
        for j in range(9 - len(hint) + 1):
            hint_locations.append(
                And(
                    *[board[i][j + k] == hint[k] for k in range(len(hint))],
                )
            )
    s.add(Or(hint_locations))

# add down hints
for hint in down_hints:
    hint_locations = []
    for j in range(9):
        for i in range(9 - len(hint) + 1):
            hint_locations.append(
                And(
                    *[board[i + k][j] == hint[k] for k in range(len(hint))],
                )
            )
    s.add(Or(hint_locations))

# check satisfiability
if s.check() == sat:
    while s.check() == sat:
        m = s.model()
        result = [[chr(m[board[i][j]].as_long()) for j in range(9)] for i in range(9)]
        for row in result:
            print(''.join(row).upper())
        print("=" * 20)
        s.add(Or([board[i][j] != m[board[i][j]] for i in range(9) for j in range(9)]))
else:
    print("No solution found")
    print(s.unsat_core())
    print(s.statistics())