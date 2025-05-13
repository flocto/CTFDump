from collections import Counter
from queue import PriorityQueue

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, nxt):
        if self.freq == nxt.freq:
            return self.symbol < nxt.symbol

        return self.freq < nxt.freq


def get_codes(codes, node=None, val=""):
    if node:
        if not node.left and not node.right:
            codes[node.symbol] = val
        else:
            get_codes(codes, node.left, val + '0')
            get_codes(codes, node.right, val + '1')


def compress(s: str) -> str:
    cnt = Counter(s)
    codes = {}

    pq = PriorityQueue()
    for element in cnt:
        pq.put(Node(cnt[element], element))

    n_nodes = len(cnt)
    while n_nodes > 1:
        left = pq.get()
        right = pq.get()
        new = Node(left.freq + right.freq,
                   min(left.symbol, right.symbol), left, right)
        pq.put(new)
        n_nodes -= 1

    get_codes(codes, node=pq.get())

    cmprsd = ""
    for c in s:
        cmprsd += codes[c]

    return cmprsd, codes
    # return cmprsd

def decompress(code: str, codes: dict) -> str:
    rev_codes = {v: k for k, v in codes.items()}

    decompressed = ""
    code_so_far = ""
    for bit in code:
        code_so_far += bit
        if code_so_far in rev_codes:
            decompressed += rev_codes[code_so_far]
            code_so_far = ""

    return decompressed


# )
# msg = 'flag{https://www.youtube.com/watch?v=tXTKX1bDX3s}'
# print(Counter(msg), ''.join(sorted(set(msg))))
# compressed, codes = compress(msg)
# print(len(set(msg)), len(msg), len(compressed), compressed, codes)
# print(decompress(compressed, codes))

# for c, code in codes.items():
#     if len(code) <= 4:
#         print(c, code)

cmp = '1101011101111100011011001000111000010011110110000101000010101010110110111001010001111000010010001101111110100100101100111110111010010101111000001110011110010101011111110100110101110011110001001101011010000101110101100100011111001101001'

chars = './03:=?BCRVabcehmoprstuvwy'
start =   'flag{https://www.youtube.com/watch?v=03BCRVr'

import itertools
from tqdm import tqdm
for rest in tqdm(list(itertools.combinations_with_replacement(chars, 4))):
    rest = ''.join(rest)
    msg = start + rest + '}'
    compressed, codes = compress(msg)
    if len(compressed) != 235:
        continue    

    # print(len(set(msg)), len(msg), len(compressed), compressed, codes)
    dec = decompress(cmp, codes)
    if dec.startswith('flag{https://www.youtube.com'):
        print(msg, dec)
        break
        