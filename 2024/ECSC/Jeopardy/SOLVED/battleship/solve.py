from pwn import remote
from tqdm import trange
# nc battleship.challs.jeopardy.ecsc2024.it 47016
r = remote('battleship.challs.jeopardy.ecsc2024.it', 47016)

for i in range(150):
    r.sendlineafter(b'(x y): ', f'{i} {i}'.encode())

leaks = []
N = 25
for i in range(N):
    r.recvuntil(b'tries to hit ')
    leak = r.recvline().strip().decode()[1:-4].split()
    leaks.append(int(leak[0]))
    leaks.append(int(leak[1]))
    r.sendlineafter(b'(x y): ', b'0 0')

state = leaks
print(state)

def unclock_prng(state):
    # out = (293 * (361 * (state[0x17] + state[0]) + 0x83)) & 0x1ff
    out = state[-1]
    c = state[0x16]

    good = []
    for x in range(512):
        test = (293 * (361 * (c + x) + 0x83)) & 0x1ff
        if test == out:
            # print('found', x)
            good.append(x)

    if len(good) == 1:
        return good[0], [good[0]] + state[:-1]

    print('wtf not found')

outs = []
for i in range(300):
    out, state = unclock_prng(state)
    outs.insert(0, out)

for i in trange(150):
    x, y = outs[i*2], outs[i*2+1]
    r.sendlineafter(b'(x y): ', f'{x} {y}'.encode())

r.interactive()