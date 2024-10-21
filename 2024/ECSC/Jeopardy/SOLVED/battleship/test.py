# from pwn import remote
# import z3
# # nc battleship.challs.jeopardy.ecsc2024.it 47016
# r = remote('battleship.challs.jeopardy.ecsc2024.it', 47016)

# for i in range(150):
#     r.sendlineafter(b'(x y): ', f'{i} {i}'.encode())

# leaks = []
# N = 24
# for i in range(N):
#     r.recvuntil(b'tries to hit ')
#     leak = r.recvline().strip().decode()[1:-4].split()
#     leaks.append(int(leak[0]))
#     leaks.append(int(leak[1]))
#     r.sendlineafter(b'(x y): ', b'0 0')

# print(leaks)

# s = z3.Solver()
# original_state = [z3.BitVec(f'state_{i}', 32) for i in range(32)]

# for st in original_state:   
#     s.add(st >= 0)
#     s.add(st < 0x200)

# def clock_prng(state):
#         # int32_t out = (_293 * (_361 * (state[0x17] + state[0]) + 0x83)) & 0x1ff
#     out = (293 * (361 * (state[0x17] + state[0]) + 0x83)) & 0x1ff
#     out_state = state[1:]
#     out_state.append(out)
#     return out, out_state

# state = original_state
# for l in leaks:
#     out, out_state = clock_prng(state)
#     s.add(out == l)
#     state = out_state

# if s.check() == z3.sat:
#     m = s.model()
#     state = [m[original_state[i]].as_long() for i in range(len(original_state))]
#     print(state)
    
# else:
#     print('unsat')

leaks = [65, 267, 257, 236, 5, 63, 189, 453, 32, 459, 427, 395, 310, 321, 12, 237, 18, 251, 322, 164, 493, 135, 8, 418, 445, 353, 327, 189, 54, 253, 443, 28, 252, 151, 188, 380, 437, 393, 235, 388, 325, 329, 119, 510, 411, 326, 37, 502]

state = leaks[-32:]
print(state)
print(leaks[:-32])

print((293 * (361 * (state[0x18] + 237) + 0x83)) % 0x200)

def unclock_prng(state):
    # out = (293 * (361 * (state[0x17] + state[0]) + 0x83)) & 0x1ff
    out = state[-1]
    c = state[0x16]

    good = []
    for x in range(512):
        test = (293 * (361 * (c + x) + 0x83)) & 0x1ff
        if test == out:
            print('found', x)
            good.append(x)

    if len(good) == 1:
        return good[0], [good[0]] + state[:-1]

    print('wtf not found')

outs = []
for i in range(8):
    out, state = unclock_prng(state)
    outs.insert(0, out)

print(outs)

r.interactive()