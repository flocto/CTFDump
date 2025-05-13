# from sudoku import Sudoku

orig = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
         [0, 0, 0, 0, 0, 3, 0, 8, 5], 
         [0, 0, 1, 0, 2, 0, 0, 0, 0], 
         [0, 0, 0, 5, 0, 7, 0, 0, 0], 
         [0, 0, 4, 0, 0, 0, 1, 0, 0], 
         [0, 9, 0, 0, 0, 0, 0, 0, 0], 
         [5, 0, 0, 0, 0, 0, 0, 7, 3], 
         [0, 0, 2, 0, 1, 0, 0, 0, 0], 
         [0, 0, 0, 0, 4, 0, 0, 0, 9]]

# puzzle = Sudoku(3, 3, board=board)
# puzzle = puzzle.solve()
# puzzle.show_full()
# board = puzzle.board

board = '987654321246173985351928746128537694634892157795461832519286473472319568863745219'

# print(''.join([str(x) for row in board for x in row]))

# transpose
# board = [[board[j][i] for j in range(9)] for i in range(9)]
# print(''.join([str(x) for row in board for x in row]))

for i in range(9):
    for j in range(9):
        if orig[i][j] != 0:
            continue
        print(f'{j} {i} {board[i*9+j]}', end=' ')