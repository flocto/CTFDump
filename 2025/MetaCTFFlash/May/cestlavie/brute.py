import gdb


def brute(guess):
    # print(f'Guess: {guess}')
    # gdb.execute(f'ignore 1 {(len(guess) - 2) * 2}')
    guess = guess.ljust(32, 'A')
    open('guess.txt', 'w').write(guess)
    gdb.execute('run chal.bin < guess.txt')

    nums = []
    for i in range(32):
        ecx = gdb.parse_and_eval('$ecx')
        ecx = int(ecx)
        # nums.append(ecx)

        # rsi + rdx * 4
        rsi = int(gdb.parse_and_eval('$rsi'))
        rdx = int(gdb.parse_and_eval('$rdx'))
        mem = gdb.inferiors()[0].read_memory(rsi + rdx * 4, 4)
        mem = int.from_bytes(mem, 'little')
        # nums.append((ecx, mem))
        if ecx != mem:
            return i

        gdb.execute('c')
        gdb.execute('c')

    print(nums, len(nums))

# guess = 'Meta1234ABCD5678efgh4321EFGH8765'
known = 'MetaCTF{In5an3_1n_7h'
alpha = '}_abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
while len(known) < 32:
    for c in alpha:
        guess = known + c
        r = brute(guess)
        # print(i, r)
        if r > len(known):
            print(f'Found: {known + c}')
            known += c