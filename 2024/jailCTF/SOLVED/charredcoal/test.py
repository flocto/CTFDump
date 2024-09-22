import subprocess

# hmm = []
# for c in range(128, 256):
#     print(c, chr(c), ord(chr(c)))

#     inp = f'{c:02x} {chr(c)*3} {ord(chr(c))} 0 1 2 3 4 5 6'
#     with subprocess.Popen(["python3", "Charcoal/charcoal.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
#         out = proc.communicate(input=inp.encode())[0].decode()
#         # print(proc.communicate(input=inp.encode())[0].decode())
#         if inp not in out:
#             print(out)
#             hmm.append(c)

# print(hmm)

hmm = [164, 166, 167, 171, 172, 177, 178, 179, 180, 182, 183, 185, 187, 191, 215, 247]

# ¤¦§«¬±²³´¶·¹»¿×÷

import random

for _ in range(1000):
    # pick 5 random ones
    c = random.choices(hmm, k=5)
    # c = random.choices(range(256), k=5)
    inp = f'{"".join(chr(i) for i in c)}¦__class__'
    with subprocess.Popen(["python3", "Charcoal/charcoal.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        out = proc.communicate(input=inp.encode())[0].decode()
        if inp not in out:
            print(inp)
            print(out)
            