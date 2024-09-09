from lights_out import get_solution
from pwn import remote
# nc be.ax 32421
r = remote("be.ax", 32421)

r.recvline_contains(b'Lights Out Board:')
board = r.recvuntil(b'Your Solution: ').decode().split('\n')[2:-3]
n = len(board)
print(board, n, len(board[0]))

vec = []
for row in board:
    for c in row:
        vec.append(1 if c == '#' else 0)

solution = get_solution(vec, n)
r.sendline(solution.encode())
r.interactive()