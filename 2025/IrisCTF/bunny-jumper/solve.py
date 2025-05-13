from base64 import b64decode as b64d, b64encode as b64e
import z3
x = [
    "dW1wanVrcGp",
    151986214,
    "dW1wanZtcGp",
    168894767,
    "dW1wahVtcGp",
    143414,
    "dW1wanVtEGp",
    202515241,
    "dW1x6nVtcGp",
    219753011,
    "dW1wcn89cGp",
    268849,
    "dW1xKnVucSp",
    18095146,
    "dW1xKhU9cGp",
    35464242,
    "dW1wOnVsMAp",
    51128620,
    "dW1wQnBtaGp",
    51782960,
    "dW1x6zVv8Gp",
    68360487,
    "dW1wCnVt1Wp",
    85665324,
    "dW1waXVv+mp",
    84281399,
    "dW1xL3ZtcGp",
    102047534,
    "dW1wfnVtEG9",
    253767992,
    "dW1x6nVFcH5",
    118959923,
    "dW1wanfucH5",
    119284279,
    "dW1xKPZtcGp",
    135141663,
    "dW1xKiVtdmp",
    152903206,
    "dW1xKtVtdmp",
    153103667,
    "dW1xKn9ucGp",
    168895531,
    "dW1xL3VucGp",
    185603370,
    "dW1x6PVtWGp",
    236723758,
    "dW1wCnVFcG9",
    286799160,
    "dW1xLHXNcGp",
    387656501,
    "dW1xKnVFWH5",
    320086583,
    "dW1xKnVFcS9",
    303307048,
    "dW1wQtXNWGp",
    170208564,
]

pref = b'anVtcGp1bXBq'
base = pref + b'dW1wanVtcGp='

def get_parts(wanted):
    wanted = pref + wanted + b'='
    wanted = b64d(wanted)

    cur = b64d(base)

    # print(wanted)
    # print(cur)

    parts = []

    for i in range(len(wanted)):
        if wanted[i] != cur[i]:
            # print(bin(wanted[i] ^ cur[i])[2:].zfill(8))
            for j in range(8):
                if (wanted[i] >> (7 - j)) & 1 != (cur[i] >> (7 - j)) & 1:
                    # print(i * 8 + j, i, j)
                    parts.append((i * 8 + j, i, j))
    return parts

flag = [z3.BitVec(f"flag_{i}", 8) for i in range(57)]
s = z3.Solver()

for i in range(len(x) - 2, -1, -2):
    wanted = x[i].encode()
    parts = get_parts(wanted)
    n = x[i + 1]
    idxs = [n >> (8 * i) & 0xff for i in range(4)][::-1]
    # print(wanted, idxs, parts)

    pairs = [(parts[i][0], parts[i + 1][0]) for i in range(0, len(parts), 2)]
    freq = {}
    offset = 0
    for a, b in pairs:
        c = chr(a - offset)
        if b - a == 1:
            freq[c] = 2
        else:
            freq[c] = 1
        offset += 4
    if len(freq) == 1:
        freq[list(freq.keys())[0]] = 4

    # print(freq)
    for c in freq:
        eqs = [flag[i] == ord(c) for i in idxs]
        s.add(z3.PbEq([(eq, 1) for eq in eqs], freq[c]))
    
print(s.check())
m = s.model()
flag = [m[flag[i]].as_long() for i in range(57)]
print(bytes(flag).decode())