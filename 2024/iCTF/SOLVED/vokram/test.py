from vm import parse, vokram_test


def to_base(n: int, base: int):
    if n == 0:
        return '0'
    digits = []
    while n:
        digits.append(str(n % base))
        n //= base
    return ''.join(reversed(digits))


def from_base(s: str, base: int):
    return sum(int(digit) * base ** i for i, digit in enumerate(reversed(s)))


enc = '12120'
program = parse(open('debug_flag.vokram').read())

txor_map = {}
starting = {}
c = 0
for pat, repl, stop in program:
    if stop:
        print('STOP', pat, repl)
        pass
    elif '🚳' in pat or '🚳' in repl:  # base3
        continue
    elif '|0' in repl:
        continue
    else:
        try:
            pa, pb = pat[-2], pat[-1]
            ra, rb = repl[0], repl[-1]
            if ra != pb or rb != pa and all(c in '012' for c in (pa, pb)):
                c += 1
                print('DIFF', pat, repl)
                if '🗓' not in repl:
                    starter = pat[:pat.index(pa)]
                    if starter not in txor_map:
                        txor_map[starter] = {}
                    txor_map[starter][(pa, pb)] = ra, rb
            # else:
            #     print('SAME', pat, repl)
        except:
            pass

print(c)
print(txor_map, len(txor_map))
print(starting, len(starting))
# edges = {}
# for pat, repl, stop in program:
#     if repl.endswith('|0'):
#         edges[pat] = repl[:-2]

# print(len(edges))

# cur = '🇫🇯'
# path = [cur]
# while cur in edges:
#     cur = edges[cur]
#     path.append(cur)

# print(len(path), path[-1])

# print(vokram_test('Xctf{abcdAAAAAAAAAAAAAAAAAAAAAAAA1234AAAAAAAA', program))

block = '10210' * 45 
head = '👃🏼|0'

# print(vokram_test(head + block, program))

txor_idxs = [0, 1, 6, 7, 8, 14, 15, 25, 26, 29, 36, 38, 43, 44, 45, 49, 51, 54, 55, 60, 61, 62, 64, 65, 68, 71, 72, 77, 78, 79, 80, 83, 84, 85, 88, 89, 95, 96, 99, 106, 107, 108, 110, 116, 120, 121, 123, 128, 133, 139, 145, 146, 148, 149, 155, 156, 164, 170, 173, 176, 180, 182, 184, 189, 197, 198, 205, 206, 210, 212, 214, 217, 218, 219, 223, 224]

# from tqdm import trange
# for i in trange(225):
#     blk = ['0' for _ in range(225)]
#     blk[i] = '1'
#     test = head + ''.join(blk)
#     ret = vokram_test(test, program)
#     # print(vokram_test(test, program))
#     if ret[-1] == '1':
#         txor_idxs.append(i)

print(txor_idxs, len(txor_idxs))

def txor(a, b):
    return (a + b) % 3

def rotate_forward(state):
    txors = [int(state[i]) for i in txor_idxs]
    s = txors[0]
    for i in range(1, len(txors)):
        s = txor(s, txors[i])
    return state[1:] + str(s)

def rotate_backward(state):
    for i in range(3):
        tmp = str(i) + state[:-1]
        if rotate_forward(tmp) == state:
            return tmp
    
    print('wtf error')
    exit()

state = '121202121112120011001220110022222210011011122110212111121120221102221202120001000021001211111001022220212121021021001200021021221012012012122121211011022112202122010221220201000102111111000120202200100201021111120102201200011'
print(state)

for _ in range(1337):
    state = rotate_backward(state)

print(state)
flag = ''
for i in range(0, len(state), 5):
    flag += chr(from_base(state[i:i+5], 3))
print(flag)